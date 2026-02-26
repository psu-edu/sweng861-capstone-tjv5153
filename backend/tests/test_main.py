import asyncio
from urllib import request
from dotenv import load_dotenv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient
import httpx
import os
import pytest
import sys
from unittest.mock import MagicMock
from unittest.mock import AsyncMock

from pytest_mock import mocker


sys.path.insert(0, "../backend")
from main import FRONTEND_URL
from main import app
from main import isAuthenticated_officer
from main import isAuthenticated
import main as backend_main
import LicensePlateRecognitionAPI
import ticketsDb_utils
import userDb_utils


load_dotenv()
OKTA_URL=os.getenv("OKTA_URL")
OKTA_CLIENT_ID=os.getenv("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET=os.getenv("OKTA_CLIENT_SECRET")
BACKEND_URL=os.getenv("BACKEND_URL")
FRONTEND_URL=os.getenv("FRONTEND_URL")
USERS_DB=os.getenv("USERS_DB")
TICKETS_DB=os.getenv("TICKETS_DB")
TEST_TOKEN=os.getenv("TEST_TOKEN")
OFFICERS=os.getenv("OFFICERS")
API_TOKEN=os.getenv("API_TOKEN")

metadata = httpx.get(f"{OKTA_URL}/.well-known/openid-configuration").json() 
authorization_url = metadata["authorization_endpoint"] 
token_url = metadata["token_endpoint"] 

client = TestClient(backend_main.app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.content is not None

def test_check_license_plate_Pass(mocker):

    fakeLicensePlate = "TEST123"

    # Mock the getLicensePlateFromImage function to return a specific license plate
    mocker.patch('LicensePlateRecognitionAPI.getLicensePlateFromImage', return_value=fakeLicensePlate)
    
    # Mock the checkIfUserHasParkingPass function to return True
    mocker.patch('userDb_utils.checkIfUserHasParkingPass', return_value=True)

    # Send a POST request to the /checkLicensePlate endpoint with a test image
    with open("testLicensePlates/demo.jpg", "rb") as img_file:
        response = client.post("/checkLicensePlate", files={"file": ("demo.jpg", img_file, "image/jpeg")})
    
    # Assert that the response is correct
    assert response.status_code == 200
    assert response.json() == {"message": f"License plate {fakeLicensePlate} has a valid parking pass"}


def test_check_license_plate_noPass(mocker):

    fakeLicensePlate = "TEST123"

    # Mock the getLicensePlateFromImage function to return a specific license plate
    mocker.patch('LicensePlateRecognitionAPI.getLicensePlateFromImage', return_value=fakeLicensePlate)
    
    # Mock the checkIfUserHasParkingPass function to return False
    mocker.patch('userDb_utils.checkIfUserHasParkingPass', return_value=False)

    # Send a POST request to the /checkLicensePlate endpoint with a test image
    with open("testLicensePlates/demo.jpg", "rb") as img_file:
        response = client.post("/checkLicensePlate", files={"file": ("demo.jpg", img_file, "image/jpeg")})
    
    # Assert that the response is correct
    assert response.status_code == 403
    assert response.json() == {"message": f"License plate {fakeLicensePlate} does not have a valid parking pass"}

def test_revoke_parking_pass(mocker):

    # user is authenticated as an officer
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_true

    # mock authentication middleware to always pass
    mock_middleware = AsyncMock(return_value=True)
    mocker.patch('main.authentication_middleware', mock_middleware)
    mock_validateTokens = AsyncMock(return_value=True)
    mocker.patch('main.validateTokens', mock_validateTokens)

    # Mock the revokeParkingPass function to return True
    mocker.patch('userDb_utils.removeParkingPassFromUser', return_value=True)

    # Send a POST request to the /revokeParkingPass endpoint with a test license plate
    client.cookies.set("session_id", TEST_TOKEN)
    response = client.put("/revokeParkingPass/TEST123", json={"licensePlate" : "TEST123"})
    
    # Assert that the response is correct
    assert response.status_code == 200
    assert response.json() == {"message": "Parking pass revoked successfully"}

def test_revoke_parking_pass_db_fail(mocker):
    #override the isAuthenticated_officer dependency to return true
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_true

    # mock authentication middleware to always pass
    mock_middleware = AsyncMock(return_value=True)
    mocker.patch('main.authentication_middleware', mock_middleware)
    mock_validateTokens = AsyncMock(return_value=True)
    mocker.patch('main.validateTokens', mock_validateTokens)

    # Parking pass is failed to be revoked in the database
    mocker.patch('userDb_utils.removeParkingPassFromUser', return_value=False)

    # Send a POST request to the /revokeParkingPass endpoint with a test license plate
    client.cookies.set("session_id", TEST_TOKEN)
    response = client.put("/revokeParkingPass/TEST123", json={"licensePlate" : "TEST123"})
    
    # Assert that the response is correct
    assert response.status_code == 500
    assert response.json() == {"error": "Failed to revoke parking pass"}
    app.dependency_overrides.clear()

def test_revoke_parking_pass_not_officer(mocker):
    #override the isAuthenticated_officer dependency to return False
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_false

    # mock authentication middleware to always pass
    mock_middleware = AsyncMock(return_value=True)
    mocker.patch('main.authentication_middleware', mock_middleware)
    mock_validateTokens = AsyncMock(return_value=True)
    mocker.patch('main.validateTokens', mock_validateTokens)

    # Send a POST request to the /revokeParkingPass endpoint with a test license plate
    client.cookies.set("session_id", TEST_TOKEN)
    response = client.put("/revokeParkingPass/TEST123", json={"licensePlate" : "TEST123"})
    
    # Assert that the response is correct
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}
    app.dependency_overrides.clear()

def test_remove_ticket(mocker):
    # user is authenticated as an officer
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_true

    mocker.patch('ticketsDb_utils.removeTicket', return_value=True)

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.delete("/removeTicket/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket removed successfully"}

def test_remove_ticket_ticket_dne(mocker):
    # user is authenticated as an officer
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_true

    mocker.patch('ticketsDb_utils.removeTicket', return_value=False)

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.delete("/removeTicket/1")
    assert response.status_code == 500
    assert response.json() == {"error": "Failed to remove ticket"}

def test_remove_ticket_ticket_not_officer(mocker):
    # user is authenticated as an officer
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_false

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.delete("/removeTicket/1")
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}

def test_add_ticket(mocker):
    # user is authenticated as an officer
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_true

    mocker.patch('ticketsDb_utils.addTicket', return_value=True)

    mocker.patch('main.validateTokens', return_value=True)

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.post("/addTicket", json={"ticketNumber" : "TEST123", "licensePlate" : "TEST123", "issueDate" : "2023-01-01", "violation" : "Test Violation", "fineAmount" : 50.0, "officerName" : "Officer Test"})
    assert response.status_code == 200
    assert response.json() == {"message": "Ticket added successfully"}

def test_add_ticket_fail(mocker):
    # user is authenticated as an officer
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_true

    mocker.patch('ticketsDb_utils.addTicket', return_value=False)

    mocker.patch('main.validateTokens', return_value=True)

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.post("/addTicket", json={"ticketNumber" : "TEST123", "licensePlate" : "TEST123", "issueDate" : "2023-01-01", "violation" : "Test Violation", "fineAmount" : 50.0, "officerName" : "Officer Test"})
    assert response.status_code == 500
    assert response.json() == {"error": "Failed to add ticket"}

def test_add_ticket_not_officer(mocker):
    # user is authenticated as an officer
    app.dependency_overrides[isAuthenticated_officer] = override_isAuthenticated_officer_false

    mocker.patch('ticketsDb_utils.addTicket', return_value=True)

    mocker.patch('main.validateTokens', return_value=True)

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.post("/addTicket", json={"ticketNumber" : "TEST123", "licensePlate" : "TEST123", "issueDate" : "2023-01-01", "violation" : "Test Violation", "fineAmount" : 50.0, "officerName" : "Officer Test"})
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}

def test_get_parking_pass(mocker):
    app.dependency_overrides[isAuthenticated] = override_isAuthenticated_user_true

    mocker.patch('userDb_utils.addParkingPassToUser', return_value=True)

    mocker.patch('main.validateTokens', return_value=True)

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.post("/parkingPass/TEST123", json={"licensePlate" : "TEST123"})
    assert response.status_code == 200
    assert response.json() == {"message": "Parking pass added successfully"}

def test_get_parking_pass_fail(mocker):
    app.dependency_overrides[isAuthenticated] = override_isAuthenticated_user_true

    mocker.patch('userDb_utils.addParkingPassToUser', return_value=False)

    mocker.patch('main.validateTokens', return_value=True)

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.post("/parkingPass/TEST123", json={"licensePlate" : "TEST123"})
    assert response.status_code == 500
    assert response.json() == {"error": "Failed to add parking pass"}

def test_get_parking_pass_not_authenticated(mocker):
    app.dependency_overrides[isAuthenticated] = override_isAuthenticated_user_false

    client.cookies.set("session_id", TEST_TOKEN)
    response = client.post("/parkingPass/TEST123", json={"licensePlate" : "TEST123"})
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}

def test_check_tickets(mocker):
    app.dependency_overrides[isAuthenticated] = override_isAuthenticated_user_true

    mocker.patch('ticketsDb_utils.checkIfLicensePlateHasTicket', return_value=[{"ticketNumber" : "TEST123", "licensePlate" : "TEST123", "issueDate" : "2023-01-01", "violation" : "Test Violation", "fineAmount" : 50.0, "officerName" : "Officer Test"}])
    
    response = client.get("/checkTickets/TEST123")
    
    assert response.status_code == 200
    assert response.json() == {"tickets": [{"ticketNumber" : "TEST123", "licensePlate" : "TEST123", "issueDate" : "2023-01-01", "violation" : "Test Violation", "fineAmount" : 50.0, "officerName" : "Officer Test"}]}

def test_check_tickets_no_tickets(mocker):
    app.dependency_overrides[isAuthenticated] = override_isAuthenticated_user_true

    mocker.patch('ticketsDb_utils.checkIfLicensePlateHasTicket', return_value=[])
    
    response = client.get("/checkTickets/TEST123")

    assert response.status_code == 200
    assert response.json() == {"message": "License plate TEST123 has no tickets"}

def test_state_check():
    assert backend_main.verifyStatePostAuth("login") is True
    assert backend_main.verifyStatePostAuth("invalid_state") is False

def override_isAuthenticated_user_false():
    return False

def override_isAuthenticated_user_true():
    return True

def override_isAuthenticated_officer_false():
    return False

def override_isAuthenticated_officer_true():
    return True