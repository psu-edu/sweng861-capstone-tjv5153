
import sys
from unittest.mock import MagicMock, Mock

sys.path.insert(0, "../backend")
import LicensePlateRecognitionAPI
from LicensePlateRecognitionAPI import demo_image
demo_image_plate = "pl8rec"

def test_license_plate_recognition_api():

    plateStr = LicensePlateRecognitionAPI.getLicensePlateFromImage(demo_image)

    assert plateStr == demo_image_plate

def test_license_plate_recognition_api_bad_stat(mocker):
    mocker.patch('httpx.post', return_value=mocker.Mock(status_code=500))

    plateReturn = LicensePlateRecognitionAPI.getLicensePlateFromImage(demo_image)

    assert plateReturn == None

def test_license_plate_recognition_api_no_data(mocker):
    response = Mock()
    response.status_code = 201
    response.json.return_value = {"results":[]}
    mocker.patch('httpx.post', return_value=response)

    plateReturn = LicensePlateRecognitionAPI.getLicensePlateFromImage(demo_image)

    assert plateReturn == None

