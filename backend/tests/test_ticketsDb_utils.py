import sqlite3
import os
import pytest
import sys
from unittest.mock import MagicMock
from pytest_mock import mocker

sys.path.insert(0, "../backend")

import ticketsDb_utils


def test_add_ticket(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    FakeTicket = ticketsDb_utils.Ticket(
        ticketNumber="test_ticket",
        licensePlate="test_license_plate",
        issueDate="2024-01-01",
        violation="test_violation",
        fineAmount=100.0,
        officerName="test_officer"
    )
    add_ticket_result = ticketsDb_utils.addTicket(FakeTicket)

    assert fake_conn.cursor().execute.call_count == 1
    assert fake_conn.commit.call_count == 1
    assert add_ticket_result == True

def test_check_if_license_plate_has_ticket(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    db_return = [("test_ticket", "test_license_plate", "2024-01-01", "test_violation", 100.0, "test_officer")]
    fake_conn.cursor().fetchall.return_value = db_return

    tickets = ticketsDb_utils.checkIfLicensePlateHasTicket("test_license_plate")

    assert fake_conn.cursor().execute.call_count == 1
    assert fake_conn.cursor().execute.call_args[0][0] == "SELECT * FROM Tickets WHERE licensePlate = ?"
    assert fake_conn.cursor().execute.call_args[0][1] == ("test_license_plate",)
    assert tickets == [ticketsDb_utils.Ticket(ticketNumber='test_ticket', licensePlate='test_license_plate', issueDate='2024-01-01', violation='test_violation', fineAmount=100.0, officerName='test_officer')]

def test_remove_ticket(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    ticketsDb_utils.removeTicket("test_ticket")

    assert fake_conn.cursor().execute.call_count == 1
    assert fake_conn.cursor().execute.call_args[0][0] == "DELETE FROM Tickets WHERE ticketNumber = ?"
    assert fake_conn.cursor().execute.call_args[0][1] == ("test_ticket",)
    assert fake_conn.commit.call_count == 1

def test_setup_tickets_db(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    ticketsDb_utils.setupTicketsDb()

    assert fake_conn.cursor().execute.call_count == 1
    assert fake_conn.cursor().execute.call_args[0][0] == '''
        CREATE TABLE IF NOT EXISTS Tickets (
            ticketNumber TEXT PRIMARY KEY,
            licensePlate TEXT,
            issueDate TEXT,
            violation TEXT,
            fineAmount REAL,
            officerName TEXT
        )'''
    assert fake_conn.commit.call_count == 1