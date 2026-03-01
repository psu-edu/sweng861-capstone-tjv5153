import sqlite3
from dotenv import load_dotenv
import os
import pydantic

load_dotenv()
TICKETS_DB_PATH = os.getenv("TICKETS_DB")


class Ticket(pydantic.BaseModel):
    ticketNumber: str
    licensePlate: str
    issueDate: str
    violation: str
    fineAmount: float
    officerName: str

def setupTicketsDb():
    try:
        conn = sqlite3.connect(TICKETS_DB_PATH)
        print("Tickets Database connection successful")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            ticketNumber TEXT PRIMARY KEY,
            licensePlate TEXT,
            issueDate TEXT,
            violation TEXT,
            fineAmount REAL,
            officerName TEXT
        )''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Tickets Database connection failed: {e}")

def checkIfLicensePlateHasTicket(licensePlate):
    try:
        conn = sqlite3.connect(TICKETS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tickets WHERE licensePlate = ?", (licensePlate,))
        tickets = cursor.fetchall()
        conn.close()
        tickets_list = []
        for ticket in tickets:
            tickets_list.append(Ticket(
                ticketNumber=ticket[0],
                licensePlate=ticket[1],
                issueDate=ticket[2],
                violation=ticket[3],
                fineAmount=ticket[4],
                officerName=ticket[5]
            ))
        return tickets_list
    except sqlite3.Error as e:
        print(f"Failed to check tickets for license plate {licensePlate}: {e}")
        return []
    
def addTicket(Ticket):
    try:
        conn = sqlite3.connect(TICKETS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tickets (ticketNumber, licensePlate, issueDate, violation, fineAmount, officerName) VALUES (?, ?, ?, ?, ?, ?)", 
                       (Ticket.ticketNumber, Ticket.licensePlate, Ticket.issueDate, Ticket.violation, Ticket.fineAmount, Ticket.officerName))
        conn.commit()
        conn.close()
        print(f"Ticket {Ticket.ticketNumber} added successfully for license plate {Ticket.licensePlate}")
        return True
    except sqlite3.Error as e:
        print(f"Failed to add ticket {Ticket.ticketNumber} for license plate {Ticket.licensePlate}: {e}")
        return False

def removeTicket(ticketNumber):
    try:
        conn = sqlite3.connect(TICKETS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Tickets WHERE ticketNumber = ?", (ticketNumber,))
        conn.commit()
        conn.close()
        print(f"Ticket {ticketNumber} removed successfully")
        return True
    except sqlite3.Error as e:
        print(f"Failed to remove ticket {ticketNumber}: {e}")
        return False
    
def checkIfIdExists(ticketNumber):
    try:
        conn = sqlite3.connect(TICKETS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tickets WHERE ticketNumber = ?", (ticketNumber,))
        ticket = cursor.fetchone()
        conn.close()
        if ticket:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"Failed to check if ticket number {ticketNumber} exists: {e}")
        return False

#Used for testing purposes to print all tickets in the database
def print_all_tickets_database():
    try:
        conn = sqlite3.connect(TICKETS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Tickets')
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            print(f"Ticket Number: {row[0]}, License Plate: {row[1]}, Issue Date: {row[2]}, Violation: {row[3]}, Fine Amount: {row[4]}, Officer Name: {row[5]}")
    except sqlite3.Error as e:
        print(f"Failed to retrieve tickets: {e}")

print_all_tickets_database()