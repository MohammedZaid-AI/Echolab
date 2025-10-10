import asyncio
import pprint
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPClient,MCPAgent


from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

SYSTEM_PROMPT = """
You are a professional research assistant.
- Always use the MCP tools available to fetch data.
- After fetching, stop reasoning and return results.
- Do not continue thinking or looping after tool output is retrieved.
"""

async def main():
    """
    Main function to run the MCP agent.
    """
    llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro")

    

    config_file="config.json"
    client=MCPClient.from_config_file(config_file)
    agent=MCPAgent(
        client=client,
        llm=llm,
        memory_enabled=True,
        max_steps=20,
        system_prompt=SYSTEM_PROMPT
        )

    # reddit_response =await agent.run("Fetch 5 recent posts from r/SaaS. For each post, include only the top 10 comments that describe problems, struggles, or challenges (e.g., issues with pricing, scaling, growth, customer retention, marketing, or technical difficulties). Ignore generic, positive, or promotional comments. Return only the problem-focused comments along with the post title and URL")
    # pprint.pprint(reddit_response)

    # tweets = await agent.run("get_tweets('#buildinpublic', 10)")
    # pprint.pprint(tweets)
   
    # youtube_response = await agent.run("fetch_youtube_videos('krish naik vids about langchain')")
    # pprint.pprint(youtube_response)
    
    # wiki_response = await agent.run("search('OpenAI')")
    # pprint.pprint(wiki_response)   

    google_results = await agent.run("Search latest AI funding rounds in 2025 using Google Search MCP.")
    pprint.pprint(google_results)
    
    medium_results = await agent.run("Search latest articles on AI in 2025 using Medium Search MCP.")
    pprint.pprint(medium_results)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())