import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

mcp = FastMCP("twitter-mcp")

def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

@mcp.tool()
def fetch_tweets(username: str, limit: int = 5):
    """Fetch recent tweets from a given username."""
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = create_headers()
    user_resp = requests.get(url, headers=headers).json()

    if "data" not in user_resp:
        return {"error": "User not found", "response": user_resp}

    user_id = user_resp["data"]["id"]

    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={limit}&tweet.fields=created_at"
    tweets_resp = requests.get(tweets_url, headers=headers).json()

    return tweets_resp.get("data", [])

@mcp.tool()
def fetch_replies(tweet_id: str, limit: int = 10):
    """Fetch replies to a given tweet ID."""
    url = f"https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{tweet_id}&max_results={limit}&tweet.fields=author_id,created_at"
    headers = create_headers()
    resp = requests.get(url, headers=headers).json()

    return resp.get("data", [])

if __name__ == "__main__":
    mcp.run(transport="stdio")
