import requests
import os
import time
from datetime import datetime, timedelta

from sensors.models import Locality, Station, SensorReading
from django.db.models import Q
from dotenv import load_dotenv
load_dotenv()

GEONAMES_USERNAME = os.getenv("GEONAMES_USERNAME")
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

class DatabaseCitySearch:


    @staticmethod
    def get_city_suggestions(query):

        if len(query) < 2:
            return []
        cities = Locality.objects.filter(Q(name__istartswith=query))[:10]
        return [f"{city.name}, {city.voivodeship}" for city in cities]

    @staticmethod
    def get_city_details(city_name):

        city = Locality.objects.filter(name=city_name).first()
        if city:
            return {
                "name": city.name,
                "voivodeship": city.voivodeship,
                "latitude": city.latitude,
                "longitude": city.longitude,
                "population": city.population,
            }
        return None


class ApiCitySearch:

    @staticmethod
    def get_location_details(city_name, max_rows=1):
        url = f"http://api.geonames.org/searchJSON?q={city_name}&maxRows={max_rows}&style=full&lang=pl&featureClass=P&username={GEONAMES_USERNAME}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get("geonames"):
                return data["geonames"]
            else:
                return None
        else:
            return None


class FetchOpenAQLocations:
    @staticmethod
    def fetch_openaq_locations():
        limit = 1000
        page = 1
        total_fetched = 0
        headers = {"X-API-Key": OPENAQ_API_KEY}

        date_from = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

        while True:
            url = f"https://api.openaq.org/v3/locations?limit={limit}&page={page}&date_from={date_from}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if not results:
                    break

                for sensor in results:

                    supported_params = {s["parameter"]["name"] for s in sensor.get("sensors", [])}

                    Station.objects.update_or_create(
                        id=sensor["id"],
                        defaults={
                            "name": sensor["name"] if sensor["name"] else "Unknown",
                            "latitude": sensor["coordinates"]["latitude"],
                            "longitude": sensor["coordinates"]["longitude"],
                            "country": sensor["country"]["code"],
                            "source": "OpenAQ v3",
                            "supports_pm25": "pm25" in supported_params,
                            "supports_pm10": "pm10" in supported_params,
                            "supports_no2": "no2" in supported_params,
                            "supports_o3": "o3" in supported_params,
                            "supports_co": "co" in supported_params,
                            "supports_so2": "so2" in supported_params,
                            "supports_voc": "voc" in supported_params,
                        }
                    )

                total_fetched += len(results)
                print(f"Fetched {total_fetched} active sensors...")
                page += 1

                time.sleep(1)  # Avoiding exceeding API limits

            else:
                print(f"Error fetching: {response.status_code} - {response.text}")
                break

        print(f"Successfully fetched {total_fetched} active sensors in total.")


class FindNearbyStationsByCoordinates:
    @staticmethod
    def find_nearby_stations_by_coordinates(latitude, longitude , max_distance=10000):
        headers = {"X-API-Key": OPENAQ_API_KEY}
        coordinates = f"{float(latitude):.6f},{float(longitude):.6f}"
        url = f"https://api.openaq.org/v3/locations?coordinates={coordinates}&radius={max_distance}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            return results
        else:
            return []

class FetchMeasurementsByStationId:
    @staticmethod
    def fetch_latest_measurements_by_station_id(station_id):
        headers = {"X-API-Key": OPENAQ_API_KEY}
        url = f"https://api.openaq.org/v3/locations/{station_id}/latest"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])

class FetchSensorById:
    @staticmethod
    def fetch_sensor_by_id(sensor_id):
        headers = {"X-API-Key": OPENAQ_API_KEY}
        url = f"https://api.openaq.org/v3/sensors/{sensor_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])

    # def fetch_daily_measurements_by_station_id(station_id, limit=1):
    #     headers = {"X-API-Key": OPENAQ_API_KEY}
    #     url = f"https://api.openaq.org/v3/locations/{station_id}/measurements?limit={limit}"

# class FetchOpenAQMeasurements:
#     @staticmethod
#     def fetch_latest_measurements():
#         headers = {"X-API-Key": OPENAQ_API_KEY}
#         stations = list(Station.objects.values_list("id", flat=True))
#         batch_size = 1000
#
#         total_updated = 0
#
#         for i in range(0, len(stations), batch_size):
#             batch = stations[i:i+batch_size]
#             location_ids = ",".join(map(str, batch))
#
#             url = f"https://api.openaq.org/v3/measurements?location_id={location_ids}&limit=1000"
#             response = requests.get(url, headers=headers)
#
#             if response.status_code == 200:
#                 data = response.json()
#                 results = data.get("results", [])
#
#                 for measurement in results:
#                     station = Station.objects.get(id=measurement["locationId"])
#                     SensorReading.objects.create(
#                         sensor=station,
#                         parameter=measurement["parameter"],
#                         value=measurement["value"],
#                         unit=measurement["unit"],
#                         timestamp=measurement["datetime"],
#                     )
#
#                 total_updated += len(results)
#                 print(f" Fetched {len(results)} measurements... (Total of: {total_updated})")
#
#             else:
#                 print(f"Error fetching: {response.status_code} - {response.text}")
#
#             time.sleep(1)
#
#         print(f"Successfully fetched {total_updated} measurements in total.")
