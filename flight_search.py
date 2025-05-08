import time
import requests
from data_manager import DataManager
from credentials import FLIGHTS_API_GET_ENDPOINT, FLIGHTS_API_PUT_ENDPOINT_TEMPLATE, HEADER

class FlightSearch(DataManager):
    def __init__(self, flights_api_get,  flights_api_put, sheety_header): #child class inherits all params
        super().__init__(flights_api_get=flights_api_get, flights_api_put=flights_api_put,
                         sheety_header=sheety_header) #pass params to parent class
        self.flight_destinations_url = "https://test.api.amadeus.com/v1/shopping/flight-destinations"


    def flight_destinations_price_check(self):
        # 1) Retrieve Sheety information
        data = self.retrieve_information()
        if not data:
            return None

        price_list = data["prices"]
        amadeus_token = self.access_token_generator()
        amadeus_header = {
            "Authorization": f"Bearer {amadeus_token}"
        }

        results = []

        for price in price_list:
            iata_code = price.get("iataCode")
            city = price.get("city")
            lowest_price = price.get("lowestPrice")

            if not iata_code:
                continue

            flight_data = {
                "origin": iata_code,
                "maxPrice": lowest_price
            }

            time.sleep(1)
            response = requests.get(self.flight_destinations_url, params=flight_data, headers=amadeus_header)

            if response.status_code == 200:
                flight_info = response.json()
                results.append({
                    "city": city,
                    "iataCode": iata_code,
                    "flights": flight_info
                })
            else:
                print(f"Failed for {city}: {response.status_code} - {response.text}")

        return results if results else None
