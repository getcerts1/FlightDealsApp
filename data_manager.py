import time
import requests
import os

FLIGHTS_API_GET_ENDPOINT = \
    "https://api.sheety.co/29947824f08bf0ac81acc4a2e300d2f4/flightDealsSheet/prices"
FLIGHTS_API_PUT_ENDPOINT_TEMPLATE = \
    "https://api.sheety.co/29947824f08bf0ac81acc4a2e300d2f4/flightDealsSheet/prices/{row_id}"
AMADEUS_GET_IATA_ENDPOINT = \
    "https://test.api.amadeus.com/v1/reference-data/locations"

TOKEN = os.getenv("FLIGHT_DEALS_SHEET_API")

HEADER = {
    "Authorization": f"Bearer {TOKEN}"
}

class DataManager:
    def __init__(self, flights_api_get, flights_api_put, sheety_header):
        self.flights_api_get = flights_api_get
        self.flights_api_put = flights_api_put
        self.sheety_header = sheety_header

    def retrieve_information(self):
        response = requests.get(url=self.flights_api_get, headers=self.sheety_header)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def access_token_generator(self):
        response = requests.post(
            url="https://test.api.amadeus.com/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": os.getenv("AMADEUS_API_KEY"),
                "client_secret": os.getenv("AMADEUS_API_SECRET")
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        return response.json().get("access_token")

    def add_iata(self):
        data = self.retrieve_information()
        if not data:
            return

        price_list = data["prices"]
        amadeus_token = self.access_token_generator()
        amadeus_header = {
            "Authorization": f"Bearer {amadeus_token}"
        }

        for price in price_list:
            city = price["city"]
            row_id = price["id"]
            time.sleep(1)  #Avoid hitting rate limit set by amadeus

            amadeus_input = {
                "keyword": city,
                "subType": "CITY"
            }

            response = requests.get(url=AMADEUS_GET_IATA_ENDPOINT, params=amadeus_input, headers=amadeus_header)
            if response.status_code == 200:
                result = response.json()
                if result["meta"]["count"] > 0:
                    city_code = result["data"][0]["address"]["cityCode"]
                    updated_data = {
                        "price": {
                            "iataCode": city_code
                        }
                    }

                    put_url = self.flights_api_put.format(row_id=row_id)
                    put_response = requests.put(url=put_url, json=updated_data, headers=self.sheety_header)

                    if put_response.status_code == 200:
                        print(f"Updated {city} with city code {city_code}")
                    else:
                        print(f"PUT error {put_response.status_code}: {put_response.text}")
                else:
                    print(f"No city code found for {city}")
            else:
                print(f"Amadeus error for {city}: {response.status_code} {response.text}")


