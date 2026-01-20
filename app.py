import asyncio
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from mcp_use import MCPClient
from my_random import get_random_user_display


load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


final_prompt = ChatPromptTemplate.from_messages([
    (
            "system",
            """
            You are HatchUp Chat, an elite startup research assistant.

            Your task:
            - Combine information from multiple real-world sources
            - Remove duplicates and noise
            - Produce ONE clear, structured answer
            - Do NOT greet the user
            - Do NOT explain tool usage

            Structure the answer into:
            • Key insights
            • Market signals
            • Opportunities
            • Risks (if any)
            """
    ),
    (
                    "human",
                    """
                    Context:
                    {context}

                    User question:
                    {question}

                    Final answer:
                    """
    )
])


client = MCPClient.from_config_file("config.json")



async def run_searches(query: str):
    if "mcp_sessions" not in st.session_state:
        st.session_state.mcp_sessions = await client.create_all_sessions()

    sessions = st.session_state.mcp_sessions

    def fail(name, e):
        return f"[{name} MCP failed: {str(e)}]"

    try:
        reddit = await sessions["@echolab/mcp-reddit"].call(
            "query", {"q": query}
        )
    except Exception as e:
        reddit = fail("Reddit", e)

    try:
        wiki = await sessions["@echolab/mcp-wikipedia"].call(
            "search", {"query": query}
        )
    except Exception as e:
        wiki = fail("Wikipedia", e)

    try:
        google = await sessions["@echolab/mcp-google"].call(
            "search", {"query": query}
        )
    except Exception as e:
        google = fail("Google", e)

    try:
        medium = await sessions["@echolab/mcp-medium"].call(
            "search", {"query": query}
        )
    except Exception as e:
        medium = fail("Medium", e)

    return {"reddit": reddit, "wiki": wiki, "google": google, "medium": medium}




def build_context(results):
    """
    Combine raw MCP outputs into a single context string.
    """
    return f"""
                [Reddit]
                {results["reddit"]}

                [Wikipedia]
                {results["wiki"]}

                [Google]
                {results["google"]}

                [Medium]
                {results["medium"]}
"""


async def main():
    st.title("HatchUp Chat")
    st.write(get_random_user_display())

    user_query = st.text_input("Enter your query:")

    if st.button("Submit") and user_query:
        with st.spinner("Researching using live sources..."):
            results = await run_searches(user_query)

            combined_context = build_context(results)

            messages = final_prompt.format_messages(
                context=combined_context,
                question=user_query
            )

            final_answer = llm.invoke(messages).content

            st.markdown("### Answer")
            st.write(final_answer)

if __name__ == "__main__":
    asyncio.run(main())
