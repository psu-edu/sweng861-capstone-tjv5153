from datetime import datetime
from dotenv import load_dotenv
import json
import logging
import os
import sqlite3
import pydantic

#configure logging
date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
USERS_DB_PATH = os.getenv("USERS_DB")
OFFICERS = os.getenv("OFFICERS")
if OFFICERS:
    OFFICERS_LIST = json.loads(OFFICERS)
else:
    OFFICERS_LIST = []

class PassSignup(pydantic.BaseModel):
    name: str
    licensePlate: str

class User():
    def __init__(self, id, username, email, accessTime, role = 'commuter', parkingPass = False):
        self.id = id
        self.username = username
        self.email = email
        self.lastAccessTime = accessTime
        self.role = role
        self.parkingPass = parkingPass

        if self.username in OFFICERS_LIST:
            self.role = 'officer'

        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        #If user does not exist insert new record else ignore
        cursor.execute("INSERT OR IGNORE INTO users (id, username, email, lastAccessTime, createdTime, role, parkingPass) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (self.id, self.username, self.email, self.lastAccessTime, self.lastAccessTime, self.role, self.parkingPass))
        conn.commit()

        cursor = conn.cursor()
        #update last access time on each login
        cursor.execute("UPDATE users SET lastAccessTime = ? WHERE id = ?", (self.lastAccessTime, self.id))
        conn.commit()
        conn.close()

def setupUsersDb():
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        print("Users Database connection successful")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id TEXT PRIMARY KEY,
            username TEXT,
            email TEXT,
            licensePlate TEXT,
            lastAccessTime INTEGER,
            createdTime INTEGER,
            role TEXT,
            parkingPass BOOLEAN
        )''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Users Database connection failed: {e}")

def addUsertoDB(userinfo):
    result = User(id=userinfo['uid'], username=userinfo['name'], email=userinfo['email'], accessTime=userinfo['auth_time'])
    if result:
        return True
    else:        
        return False

def addParkingPassToUser(licensePlate, name):
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET parkingPass = ?, licensePlate = ? WHERE username = ?", (True, licensePlate, name))
        conn.commit()
        conn.close()
        print(f"Added parking pass for user {name} with license plate {licensePlate}")
        return True
    except sqlite3.Error as e:
        print(f"Failed to add parking pass: {e}")
        return False
    
def removeParkingPassFromUser(licensePlate : str):
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET parkingPass = ? WHERE licensePlate = ?", (False, licensePlate))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Failed to remove parking pass: {e}")
        return False

def checkIfUserHasParkingPass(licensePlate : str):
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT parkingPass FROM users WHERE licensePlate = ?", (licensePlate.upper(),))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0] == 1
        else:
            logger.warning(f"No user found with license plate: {licensePlate}")
            return False
    except sqlite3.Error as e:
        print(f"Failed to check parking pass: {e}")
        return False

def isDbUp():
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Users Database connection failed: {e}")
        return False
 
#Used for testing purposes to print all users in the database
def print_all_users_database():
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}, License Plate: {row[3]}, Last Access Time: {row[4]}, Created Time: {row[5]}, Role: {row[6]}, Parking Pass: {row[7]}")
    except sqlite3.Error as e:
        print(f"Failed to retrieve users: {e}")

print_all_users_database()