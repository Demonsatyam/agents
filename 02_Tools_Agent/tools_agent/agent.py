from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="tools_agent",
    model="gemini-2.5-flash-lite",
    description="adding up tools to the agents",
    instruction="""
        
    """,

    tools=[google_search],
)