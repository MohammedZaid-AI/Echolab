from mcp.server.fastmcp import FastMCP

mcp=FastMCP()

@mcp.tool()
async def search_tweets(query: str, count: int = 20):
    """Search for tweets matching a query or hashtag"""
    return await get_tweets(query, count)

@mcp.tool()
async def fetch_replies(tweet_id: str, count: int = 20):
    """Fetch replies for a given tweet"""
    return await get_replies_for_tweet(tweet_id, count)


if __name__ == "__main__":
    mcp.run(transport="stdio")