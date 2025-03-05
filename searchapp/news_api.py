import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news(query, max_results=5):
    """
    Fetch news articles related to the query using NewsAPI.
    """
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&pageSize={max_results}"
    
    response = requests.get(url)
    data = response.json()

    news_results = []
    if "articles" in data:
        for article in data["articles"]:
            news_results.append({
                "title": article["title"],
                "url": article["url"],
                "source": article["source"]["name"],
                "description": article.get("description", "No description available.")
            })

    return news_results
