ONLINE_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "retrieve_documents",
        "description": (
            "Search the web for documents based on the user query. "
            "Usually use this if the user is asking for information that is not in the knowledge base."
            "If the user has a typo in their query, correct it before searching."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "The user query to retrieve documents for",
                },
            },
            "required": ["search_query"],
        },
    },
}

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "retrieve_weather",
        "description": (
            "Get the weather of a specific city and date. "
            "Always use this if the user is asking for weather information."   
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to retrieve weather information for",
                },
                "date": {
                    "type": "string",
                    "description": "The date to retrieve weather information for",
                },
            },
            "required": ["city", "date"],
        },
    },
}