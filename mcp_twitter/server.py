from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("twitter-bs-scraper")

@mcp.tool()
def fetch_hashtag_tweets(hashtag: str, tweet_limit: int = 5):
    """
    Scrape recent tweets from a hashtag using Twitter web search.
    NOTE: This uses scraping, so may be less reliable than the official API.
    """
    url = f"https://nitter.net/search?f=tweets&q=%23{hashtag}&since=&until=&near="
    headers = {"User-Agent": "Mozilla/5.0"}
    
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"error": "Failed to fetch tweets", "status": resp.status_code}
    
    soup = BeautifulSoup(resp.text, "html.parser")
    tweets = []
    
    for item in soup.select(".timeline-item")[:tweet_limit]:
        text = item.select_one(".tweet-content").get_text(" ", strip=True)
        username = item.select_one(".username").get_text(strip=True)
        link = "https://nitter.net" + item.select_one("a[href*='/status/']")["href"]
        
        tweets.append({
            "username": username,
            "tweet_text": text,
            "tweet_url": link
        })
    
    return tweets

if __name__ == "__main__":
    mcp.run(transport="stdio")
