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

    twitter_response=await agent.run("Fetch 20 tweets from the hashtag #buildinpublic that are problem-style posts (tweets asking for help, reporting errors, or describing issues — e.g., containing words like “error”, “bug”, “issue”, “stuck”, “how to”, “why”, “any idea”). For each of these tweets, fetch its top 10 replies. ")
    pprint.pprint(twitter_response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
