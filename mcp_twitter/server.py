from mcp.server.fastmcp import FastMCP
import json
from twikit import Client
from typing import List, Dict
from pathlib import Path
import logging
import asyncio
import os

logger = logging.getLogger(__name__)

# Read credentials from env (.env file or system)
USERNAME = os.getenv("TWITTER_USERNAME")
EMAIL = os.getenv("TWITTER_EMAIL")
PASSWORD = os.getenv("TWITTER_PASSWORD")

# Store cookies here (make sure folder exists)
COOKIES_PATH = Path("D:/Zaids Work/EchoLab/mcp_twitter/cookies.json")

# Create MCP server
mcp = FastMCP("twitter-mcp")

# Helper function to normalize tweet data
def get_tweet_data(tweet) -> dict:
    return {
        "id": tweet.id,
        "url": f"https://twitter.com/i/web/status/{tweet.id}",
        "text": tweet.text,
        "user": getattr(tweet.user, "screen_name", None),
        "created_at": str(getattr(tweet, "created_at", "")),
    }

# Authenticate Twitter client
async def get_twitter_client() -> Client:
    client = Client("en-US")

    if COOKIES_PATH.exists():
        client.load_cookies(COOKIES_PATH)
    else:
        try:
            await client.login(
                auth_info_1=USERNAME,
                auth_info_2=EMAIL,
                password=PASSWORD,
            )
            COOKIES_PATH.parent.mkdir(parents=True, exist_ok=True)
            client.save_cookies(COOKIES_PATH)
        except Exception as e:
            logger.error(f"Failed to login: {e}")
            raise
    return client


# ---------------- TOOLS ---------------- #

@mcp.tool()
async def get_tweets(query: str, sort_by: str = "Latest", count: int = 20) -> List[dict]:
    """Search tweets by query (hashtag or keyword)."""
    try:
        client = await get_twitter_client()
        tweets = await client.search_tweet(query, sort_by, count=count)
        return [get_tweet_data(tweet) for tweet in tweets]
    except Exception as e:
        logger.error(f"Error during tweet retrieval: {e}")
        return []


@mcp.tool()
async def get_user_tweets(username: str, tweet_type: str = "Tweets", count: int = 10) -> List[dict]:
    """Get tweets from a specific user's timeline."""
    try:
        client = await get_twitter_client()
        username = username.lstrip("@")
        user = await client.get_user_by_screen_name(username)
        if not user:
            return [{"error": f"Could not find user {username}"}]

        tweets = await client.get_user_tweets(
            user_id=user.id,
            tweet_type=tweet_type,
            count=count,
        )
        return [get_tweet_data(tweet) for tweet in tweets]
    except Exception as e:
        logger.error(f"Failed to get user tweets: {e}")
        return [{"error": f"Failed to get user tweets: {e}"}]


@mcp.tool()
async def get_replies_for_tweet(tweet_id: str, count: int = 30) -> List[dict]:
    """Get replies for a specific tweet using Twikit's get_tweet_detail()."""
    try:
        client = await get_twitter_client()
        
        # Get tweet details (this includes replies)
        tweet_detail = await client.get_tweet_detail(tweet_id)
        
        if not tweet_detail or not hasattr(tweet_detail, "replies"):
            return [{"error": f"No replies found for tweet {tweet_id}"}]
        
        # Slice only the top N replies
        replies = tweet_detail.replies[:count]
        
        return [get_tweet_data(reply) for reply in replies]
    except Exception as e:
        logger.error(f"Error fetching replies for tweet {tweet_id}: {e}")
        return [{"error": f"Error fetching replies: {e}"}]



if __name__ == "__main__":
    mcp.run(transport="stdio")