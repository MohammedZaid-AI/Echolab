from mcp.server import FastMCP
import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT", "echolab-mcp-reddit/0.1")
)

mcp=FastMCP("Reddit")

@mcp.tool()
def fetch_reddit_posts_with_comments(subreddit="all", limit="5", comments_per_post="15"):
    """
    Fetch hot posts and top comments from a subreddit.
    """
    try:
        # Convert string inputs to int
        limit = int(limit)
        comments_per_post = int(comments_per_post)

        posts_data = []
        sub = reddit.subreddit(subreddit)
        submissions = sub.hot(limit=limit)

        for post in submissions:
            post_info = {
                "id": post.id,
                "title": post.title,
                "author": str(post.author) if post.author else "deleted",
                "url": f"https://reddit.com{post.permalink}",
                "score": int(post.score),
                "num_comments": int(post.num_comments),
                "created_utc": float(post.created_utc),
                "comments": []
            }

            post.comments.replace_more(limit=0)
            for comment in post.comments[:comments_per_post]:
                post_info["comments"].append({
                    "author": str(comment.author) if comment.author else "deleted",
                    "body": comment.body or "",
                    "score": int(comment.score)
                })

            posts_data.append(post_info)

        # Always return something structured
        return {"posts": posts_data}

    except Exception as e:
        return {"error": str(e), "posts": []}



if __name__ == "__main__":
    print("Reddit MCP Server is running...")
    mcp.run(transport="stdio")