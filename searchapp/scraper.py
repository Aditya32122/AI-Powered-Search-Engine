import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and search engine ID from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')



def google_search(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
    }

   

    response = requests.get(search_url, params=params)
    results = response.json()

   
    search_results = []
    if "items" in results:
        for item in results["items"]:
            title = item["title"]
            link = item["link"]
            snippet = item.get("snippet", "")
            search_results.append({"title": title, "link": link, "snippet": snippet})
    
    return search_results