import asyncio
import pprint
import os
from langchain_groq import ChatGroq
from mcp_use import MCPClient,MCPAgent
from my_random import get_random_user_display
import streamlit as st

from dotenv import load_dotenv
load_dotenv()
groq_api_key=os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

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

    

    config_file="config.json"
    client=MCPClient.from_config_file(config_file)
    agent=MCPAgent(
        client=client,
        llm=llm,
        memory_enabled=True,
        max_steps=20,
        system_prompt=SYSTEM_PROMPT
        )

    st.write(get_random_user_display()) 

    user_query=st.text_input("Enter your query:")
    button=st.button("Submit")
    if button:
        reddit_response =await agent.run(user_query)
        pprint.pprint(reddit_response)
        
        wiki_response = await agent.run(user_query)
        pprint.pprint(wiki_response)   

        google_results = await agent.run(user_query)
        pprint.pprint(google_results)
        
        medium_results = await agent.run(user_query)
        pprint.pprint(medium_results)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())