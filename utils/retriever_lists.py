ONLINE_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "retrieve_documents",
        "description": (
            "Retrieve documents from the search engine based on the user query. "
            "This tool is useful for fetching context to provide more accurate answers."
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

WEATHER_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "retrieve_weather",
        "description": (
            "Retrieve weather information from the weather API based on the user query. "
            "This tool is useful for fetching weather information for a specific location."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to retrieve weather information for",
                },
            },
            "required": ["city"],
        },
    },
}