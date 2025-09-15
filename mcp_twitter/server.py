import os
from mcp.server import FastMCP
import requests
from dotenv import load_dotenv

load_dotenv()
mcp=FastMCP("Twitter")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

@mcp.tool()
def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

def get_replies(tweet_id, limit=10):
    url = f"https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{tweet_id}&max_results={limit}&tweet.fields=author_id,created_at"
    headers = create_headers()
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    tweet_id = "1234567890123456789"
    replies = get_replies(tweet_id)
    print(replies)

if __name__ == "__main__":
    mcp.run(transport="stdio")