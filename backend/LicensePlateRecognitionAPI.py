from dotenv import load_dotenv
import os
import httpx
import logging
from datetime import datetime

#configure logging
date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

demo_image = "testLicensePlates/demo.jpg"

def getLicensePlateFromImage(image):
    regions = ["mx", "us-ca"]

    with open(image, "rb") as img_file:
        response = httpx.post(
            "https://api.platerecognizer.com/v1/plate-reader/",
            headers={"Authorization": f"Token {API_TOKEN}"},
            data=dict(regions=regions),
            files=dict(upload=img_file)
        )
    if response.status_code == 201:
        result = response.json()
        if result["results"]:
            license_plate = result["results"][0]["plate"]
            logger.info(f"License plate recognized: {license_plate}")
            return license_plate
        else:
            logger.warning("No license plate found in the image")
            return None
    else:
        logger.error(f"API request failed with status code {response.status_code}: {response.text}")
        return None


#getLicensePlateFromImage(demo_image)