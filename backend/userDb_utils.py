from dotenv import load_dotenv
import json
import os
import sqlite3

load_dotenv()
USERS_DB_PATH = os.getenv("USERS_DB")
OFFICERS = os.getenv("OFFICERS")
if OFFICERS:
    OFFICERS_LIST = json.loads(OFFICERS)
else:
    OFFICERS_LIST = []


class User():
    def __init__(self, id, username, email, accessTime, role = 'commuter'):
        self.id = id
        self.username = username
        self.email = email
        self.lastAccessTime = accessTime
        self.role = role

        if self.username in OFFICERS_LIST:
            self.role = 'officer'

        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        #If user does not exist insert new record else ignore
        cursor.execute("INSERT OR IGNORE INTO users (id, username, email, lastAccessTime, createdTime, role) VALUES (?, ?, ?, ?, ?, ?)", 
                       (self.id, self.username, self.email, self.lastAccessTime, self.lastAccessTime, self.role))
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
            role TEXT
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
    
#Used for testing purposes to print all users in the database
def print_all_users_database():
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Username: {row[1]}, Email: {row[2]}, Last Access Time: {row[3]}, Created Time: {row[4]}, Role: {row[5]}")
    except sqlite3.Error as e:
        print(f"Failed to retrieve users: {e}")