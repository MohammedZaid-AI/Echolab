from mcp_use.connectors.base import BaseConnector
import requests

class TwitterConnector(BaseConnector):
    name = "twitter"

    async def initialize(self):
        self.bearer_token = self.config.get("bearer_token")
        if not self.bearer_token:
            raise ValueError("Twitter bearer token not set in config.")
        return {"status": "initialized"}

    async def fetch_tweets(self, username: str, limit: int = 5):
        """Fetch recent tweets from a user."""
        url = f"https://api.twitter.com/2/users/by/username/{username}"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        user_resp = requests.get(url, headers=headers).json()
        user_id = user_resp["data"]["id"]

        url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={limit}"
        tweets_resp = requests.get(url, headers=headers).json()
        return tweets_resp.get("data", [])

    async def fetch_replies(self, tweet_id: str, limit: int = 10):
        """Fetch replies to a specific tweet."""
        url = f"https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{tweet_id}&max_results={limit}&tweet.fields=author_id,created_at"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        resp = requests.get(url, headers=headers).json()
        return resp.get("data", [])
