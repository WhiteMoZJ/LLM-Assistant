import json
import requests

# Define a function to retrieve documents from the search engine
def retrieve_documents(query: str) -> dict:
    # Using bochiai search API
    # Replace with the API you use
    search_url = "https://api.bochaai.com/v1/web-search"
    params = {
        "query": query,
        "freshness": "oneYear",
        "summary": True,
        "count": 10,
    }

    headers = {
        'Authorization': f"Bearer {open('config/key', 'r').read()}",
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


# def retrieve_weather(city: str) -> dict: