import json
import requests
from xpinyin import Pinyin

# Load the API keys from the configuration file
# located at ChatEngine/config/key.json
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
def retrieve_documents(search_query: str) -> dict:
    # Using bochiai search API @https://open.bochaai.com/
    # Replace with the API you use if different
    search_url = "https://api.bochaai.com/v1/web-search"
    params = {
        "query": search_query,
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
        if len(response.json()['data']['webPages']['value']) < 3:
            params = {
                "query": search_query,
                "freshness": "noLimit",
                "summary": True,
                "count": 10,
            }
            response = requests.request("POST", search_url, headers=headers, data=json.dumps(params))

    if response.status_code == 200:
        # comment out the following line to disable logging
        with open("ChatEngine/log/search_log.json", "w") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
            
        context = [{
                    "title": item['name'],
                    "url": item['url'],
                    "context": item['summary'],
                    } 
                    for item in response.json()['data']['webPages']['value']]

        return {
             "status": "success",
             "content": context
        }


def get_pinyin(name):
    s = Pinyin().get_pinyin(name).split('-')
    result = ''
    for i in range(0,len(s)):
        result = result+s[i].capitalize()
    return result

def retrieve_weather(city: str, date: str) -> dict:
    # Using WeatherMap API @https://www.weatherapi.com/
    # Replace with the API you use if different
    # check city string is chinese or english
    base_url = "http://api.weatherapi.com/v1"
    params = {
        "key": weather_key,
        "q": get_pinyin(city), # Convert the city name to pinyin if it is in Chinese
        "dt": date,
        "days": 1,
        "lang": "zh_cmn",
    }

    # Sending request to the weather API
    response = requests.get(f"{base_url}/forecast.json", params=params)
    print(response)

    if response.status_code == 200:
        data = response.json()
        context = {
            "weather": {
                "current":{
                    "description": data["current"]["condition"]["text"],
                    "temperature": {
                        "current": {
                            "value": data["current"]["temp_c"],
                            "unit": "°C"
                        },
                        "Feels like": {
                            "value": data["current"]["feelslike_c"],
                            "unit": "°C"
                        }
                    },
                    "humidity": {
                        "value": data["current"]["humidity"],
                        "unit": "%"
                    },
                    "wind_speed":{
                        "value": data["current"]["wind_kph"],
                        "unit": "km/h"
                    },
                    "precipitation": {
                        "value": data["current"]["precip_mm"],
                        "unit": "mm"
                    },
                    "uv": {
                        "value": data["current"]["uv"],
                        "unit": ""
                    }
                },
                "forecast": {
                    "description": data["forecast"]["forecastday"][0]["day"]["condition"]["text"],
                    "temperature": {
                        "max": {
                            "value": data["forecast"]["forecastday"][0]["day"]["maxtemp_c"],
                            "unit": "°C"
                        },
                        "min": {
                            "value": data["forecast"]["forecastday"][0]["day"]["mintemp_c"],
                            "unit": "°C"
                        },
                        "avg": {
                            "value": data["forecast"]["forecastday"][0]["day"]["avgtemp_c"],
                            "unit": "°C"
                        }
                    },
                    "rain": {
                        "change of rain": {
                            "value": data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"],
                            "unit": "%"
                        },
                        "precipitation": {
                            "value": data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"],
                            "unit": "mm"
                        }
                    },
                    "astro": {
                        "sunrise": data["forecast"]["forecastday"][0]["astro"]["sunrise"],
                        "sunset": data["forecast"]["forecastday"][0]["astro"]["sunset"]
                    }
                }
            },
            "last_update": data["current"]["last_updated"]
        }

        # comment out the following line to disable logging
        with open("ChatEngine/log/weather-{}-{}.json".format(city, date), "w") as f:
            json.dump(context, f, ensure_ascii=False, indent=4)

        return {
            "status": "success",
            "content": context
        }
    
# print(retrieve_weather("北京", "2025-02-07"))
# print(retrieve_documents("皮昊旋"))