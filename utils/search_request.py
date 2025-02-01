import urllib.parse
import urllib.request
import json

def fetch_wikipedia_content(search_url, search_query: str) -> dict:
    """Fetches wikipedia content for a given search_query"""
    try:
        # Search for most relevant article
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search_query,
            "srlimit": 1,
        }

        url = f"{search_url}?{urllib.parse.urlencode(search_params)}"
        with urllib.request.urlopen(url) as response:
            search_data = json.loads(response.read().decode())

        if not search_data["query"]["search"]:
            return {
                "status": "error",
                "message": f"No Wikipedia article found for '{search_query}'",
            }

        # Get the normalized title from search results
        normalized_title = search_data["query"]["search"][0]["title"]

        # Now fetch the actual content with the normalized title
        content_params = {
            "action": "query",
            "format": "json",
            "titles": normalized_title,
            "prop": "extracts",
            "exintro": "true",
            "explaintext": "true",
            "redirects": 1,
        }

        url = f"{search_url}?{urllib.parse.urlencode(content_params)}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        pages = data["query"]["pages"]
        page_id = list(pages.keys())[0]

        if page_id == "-1":
            return {
                "status": "error",
                "message": f"No Wikipedia article found for '{search_query}'",
            }

        content = pages[page_id]["extract"].strip()
        return {
            "status": "success",
            "content": content,
            "title": pages[page_id]["title"],
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# Define tool for LM Studio
WIKI_TOOL = {
    "type": "function",
    "function": {
        "name": "fetch_wikipedia_content",
        "description": (
            "Search Wikipedia and fetch the introduction of the most relevant article. "
            "Always use this if the user is asking for something that is likely on wikipedia. "
            "If the user has a typo in their search query, correct it before searching."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "Search query for finding the Wikipedia article",
                },
            },
            "required": ["search_query"],
        },
    },
}