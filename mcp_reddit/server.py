from mcp.server import FastMCP, stdio
import praw
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("USER_AGENT", "echolab-mcp-reddit/0.1")
)
mcp=FastMCP("Reddit")

@mcp.tool()
def fetch_reddit_posts_with_comments(subreddit="all", limit=5, comments_per_post=15):
    """
    Fetch hot posts and top comments from a subreddit.
    :param subreddit: subreddit name (default: all)
    :param limit: number of posts
    :param comments_per_post: number of comments to fetch per post
    :return: list of dicts with post + comments
    """
    posts_data = []
    try:
        sub = reddit.subreddit(subreddit)
        submissions = sub.hot(limit=limit)

        for post in submissions:
            post_info = {
                "id": post.id,
                "title": post.title,
                "author": str(post.author) if post.author else "deleted",
                "url": f"https://reddit.com{post.permalink}",
                "score": post.score,
                "num_comments": post.num_comments,
                "created_utc": post.created_utc,
                "comments": []
            }

            post.comments.replace_more(limit=0)  # flatten "load more"
            for comment in post.comments[:comments_per_post]:
                post_info["comments"].append({
                    "author": str(comment.author) if comment.author else "deleted",
                    "body": comment.body if comment.body else "",
                    "score": comment.score
                })

            posts_data.append(post_info)

    except Exception as e:
        print(f"Error fetching from r/{subreddit}: {e}")

    return posts_data


if __name__ == "__main__":
    mcp.run(transport=stdio)