import json
import requests
from .tools import get_pinyin

# Load the API keys from the configuration file
# located at {project root folder}/config/key.json
# Format:
# {
#     "search_key": "YOUR_SEARCH_API_KEY",
#     "weather_key": "YOUR_WEATHER_API_KEY"
# }
with open("ChatEngine/config/key.json", "r") as f:
    key = json.load(f)
    search_key = key["search_key"]
    weather_key = key["weather_key"]

# Define a function to retrieve documents from the search engine
def retrieve_documents(query: str) -> dict:
    # Using bochiai search API @https://open.bochaai.com/
    # Replace with the API you use if different
    search_url = "https://api.bochaai.com/v1/web-search"
    params = {
        "query": query,
        "freshness": "oneYear",
        "summary": True,
        "count": 10,
    }

    headers = {
        'Authorization': f"Bearer {search_key}",
        'Content-Type': 'application/json'
    }

    # Sending request to the search API
    response = requests.request("POST", search_url, headers=headers, data=json.dumps(params))

    if response.status_code == 200:
        # with open("./text.json","w") as f:
        #     json.dump(response.json(), f, ensure_ascii=False, indent=4)
        context = "\n".join([item['summary'] for item in response.json()['data']['webPages']['value']])  # Combine the documents into a single string
        return {
             "status": "success",
             "content": context
        }


def retrieve_weather(city: str, date: str) -> dict:
    # Using WeatherMap API @https://www.weatherapi.com/
    # Replace with the API you use if different
    # check city string is chinese or english
    if city.encode('UTF-8').isalpha():
        city = get_pinyin(city)
    base_url = "http://api.weatherapi.com/v1"
    params = {
        "key": weather_key,
        "q": city,
        "dt": date,
        "days": 3,
        "lang": "zh_cmn",
    }

    # Sending request to the weather API
    response = requests.get(f"{base_url}/forecast.json", params=params)

    if response.status_code == 200:
        data = response.json()
        context = {
            "city": data["location"]["name"],
            "forcast": [
                {
                    "date": item["date"],
                    "condition": item["day"]["condition"]["text"],
                    "max temperature": item["day"]["maxtemp_c"],
                    "min temperature": item["day"]["mintemp_c"],
                    "humidity": item["day"]["avghumidity"],
                    "wind": item["day"]["maxwind_kph"]
                }
                for item in data["forecast"]["forecastday"]
            ],
        }

        with open("weather.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return {
            "status": "success",
            "content": context
        }