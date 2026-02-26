import sqlite3
import os
import pytest
import sys
from unittest.mock import MagicMock
from pytest_mock import mocker

sys.path.insert(0, "../backend")

import userDb_utils

def test_add_parking_pass_to_user(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    result = userDb_utils.addParkingPassToUser("TEST_LICENSE_PLATE", "TEST_USER")
    assert fake_conn.cursor().execute.call_count == 1
    assert fake_conn.cursor().execute.call_args[0][0] == "UPDATE users SET parkingPass = ?, licensePlate = ? WHERE username = ?"
    assert fake_conn.cursor().execute.call_args[0][1] == (True, "TEST_LICENSE_PLATE", "TEST_USER")
    assert fake_conn.commit.call_count == 1

def test_remove_parking_pass_from_user(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    result = userDb_utils.removeParkingPassFromUser("TEST_LICENSE_PLATE")
    assert fake_conn.cursor().execute.call_count == 1
    assert fake_conn.cursor().execute.call_args[0][0] == "UPDATE users SET parkingPass = ? WHERE licensePlate = ?"
    assert fake_conn.cursor().execute.call_args[0][1] == (False, "TEST_LICENSE_PLATE")
    assert fake_conn.commit.call_count == 1

def test_check_if_user_has_parking_pass(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    fake_conn.cursor().fetchone.return_value = (1,)
    result = userDb_utils.checkIfUserHasParkingPass("TEST_LICENSE_PLATE")
    assert fake_conn.cursor().execute.call_count == 1
    assert fake_conn.cursor().execute.call_args[0][0] == "SELECT parkingPass FROM users WHERE licensePlate = ?"
    assert fake_conn.cursor().execute.call_args[0][1] == ("TEST_LICENSE_PLATE",)
    assert result == True

    fake_conn.cursor().fetchone.return_value = (0,)
    result = userDb_utils.checkIfUserHasParkingPass("TEST_LICENSE_PLATE")
    assert result == False

def test_users_class(mocker):
    fake_conn = MagicMock()
    mocker.patch('sqlite3.connect', return_value=fake_conn)

    user = userDb_utils.User(id="TEST_ID", username="TEST_USER", email="TEST_EMAIL", accessTime=1234567890)
    assert user.id == "TEST_ID"
    assert user.username == "TEST_USER"
    assert user.email == "TEST_EMAIL"

    assert fake_conn.cursor().execute.call_count == 2