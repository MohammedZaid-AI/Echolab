from mcp.server import FastMCP
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
load_dotenv()
import os
mcp = FastMCP("YouTube MCP Server")

# Initialize YouTube API client
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY, cache_discovery=False)



def search_videos(query, max_results=5):
    """Search for YouTube videos matching a query."""
    req = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video",
        order="date",
        relevanceLanguage="en"
    )
    res = req.execute()
    videos = []
    for item in res.get("items", []):
        videos.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })
    return videos


def get_transcript(video_id):
    """Fetch transcript for a given YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except Exception:
        return ""


@mcp.tool()
def fetch_youtube_videos(query: str, count: int = 5):
    """
    Fetch recent YouTube videos and their transcripts related to a given topic or person.
    Example: "What did Sam Altman say about AI last week"
    """
    videos = search_videos(query, max_results=count)
    if not videos:
        return {"error": "No videos found for the given query."}

    results = []
    for v in videos:
        transcript = get_transcript(v["video_id"])
        results.append({
            "title": v["title"],
            "channel": v["channel"],
            "published_at": v["published_at"],
            "url": v["url"],
            "transcript": transcript or "No transcript available."
        })

    return results


if __name__ == "__main__":
    print("YouTube MCP Server is running...")
    mcp.run(transport="stdio")

