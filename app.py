import asyncio
import pprint
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPClient,MCPAgent
from random import choice

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

    user_query=input(choice(user_display_list))

    reddit_response =await agent.run(user_query)
    pprint.pprint(reddit_response)

    tweets = await agent.run(user_query)
    pprint.pprint(tweets)
   
    youtube_response = await agent.run(user_query)
    pprint.pprint(youtube_response)
    
    wiki_response = await agent.run(user_query)
    pprint.pprint(wiki_response)   

    google_results = await agent.run(user_query)
    pprint.pprint(google_results)
    
    medium_results = await agent.run(user_query)
    pprint.pprint(medium_results)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())