

import requests
from data_manager import AMADEUS_GET_IATA_ENDPOINT, TOKEN, DataInstance

"""
amadeus_input = {
    "keyword": "Kuala lampur",
    "subType": "CITY"
}

amadeus_header = {
    "Authorization": f"Bearer {DataInstance.access_token_generator()}"
}

response = requests.get(url=AMADEUS_GET_IATA_ENDPOINT, params=amadeus_input, headers=amadeus_header)
print(response.text)
"""

amadeus_input = {
    "keyword": "London",
    "subType": "CITY"
}

amadeus_token = DataInstance.access_token_generator()
amadeus_header = {
            "Authorization": f"Bearer {amadeus_token}"
}

response = requests.get(url=AMADEUS_GET_IATA_ENDPOINT, params=amadeus_input, headers=amadeus_header)
print(response.text)