import requests
import os

from sensors.models import Locality

from dotenv import load_dotenv
load_dotenv()


GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")


def get_location_details(city_name):
    url = f"http://api.geonames.org/searchJSON?q={city_name}&maxRows=1&username={GEONAMES_USERNAME}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("geonames"):
            return data["geonames"][0]
        else:
            return None
    else:
        return None


