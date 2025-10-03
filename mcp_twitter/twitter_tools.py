import os
import tweepy
from typing import List, Dict

# Load bearer token from environment
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

if not bearer_token:
    raise ValueError("⚠️ Missing TWITTER_BEARER_TOKEN in environment")

# Initialize Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

def get_tweet_data(tweet) -> Dict:
    """Format tweet data into dict"""
    return {
        "id": tweet.id,
        "text": tweet.text,
        "author_id": tweet.author_id,
        "created_at": str(tweet.created_at)
    }

async def get_tweets(query: str, count: int = 20) -> List[Dict]:
    """Search tweets by query or hashtag"""
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=min(count, 100),  # API limit is 100
            tweet_fields=["id", "text", "author_id", "created_at"]
        )

        if not response.data:
            return [{"error": f"No tweets found for query '{query}'"}]

        return [get_tweet_data(tweet) for tweet in response.data]

    except Exception as e:
        return [{"error": f"Error during tweet retrieval: {e}"}]


async def get_replies_for_tweet(tweet_id: str, count: int = 20) -> List[Dict]:
    """Fetch replies for a given tweet"""
    try:
        # Trick: search for tweets where conversation_id = tweet_id
        response = client.search_recent_tweets(
            query=f"conversation_id:{tweet_id}",
            max_results=min(count, 100),
            tweet_fields=["id", "text", "author_id", "created_at"]
        )

        if not response.data:
            return [{"error": f"No replies found for tweet {tweet_id}"}]

        return [get_tweet_data(tweet) for tweet in response.data]

    except Exception as e:
        return [{"error": f"Error fetching replies: {e}"}]