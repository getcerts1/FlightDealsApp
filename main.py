#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests

from data_manager import DataManager
from credentials import FLIGHTS_API_GET_ENDPOINT, FLIGHTS_API_PUT_ENDPOINT_TEMPLATE, HEADER
from flight_search import FlightSearch


#print(DataInstance.retrieve_information())


instance1 = FlightSearch(FLIGHTS_API_GET_ENDPOINT, FLIGHTS_API_PUT_ENDPOINT_TEMPLATE, HEADER)

#print(instance1.flight_destinations_price_check())


data = {
    "origin": "LON",
    "maxPrice": 400
}

amadeus_token = instance1.access_token_generator()
amadeus_header = {
            "Authorization": f"Bearer {amadeus_token}"
        }


response = requests.get(url="https://test.api.amadeus.com/v1/shopping/flight-destinations",
                        params=data, headers=amadeus_header)

if response.status_code == 200:
    print("success")

else:
    print(f"error code: {response.status_code}\nerror message: {response.text}")

print(response)