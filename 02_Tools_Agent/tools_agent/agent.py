from google.adk.agents import Agent
from google.adk.tools import google_search
from datetime import datetime
import pytz






# function that tells the agent to return the current time, date (DD-MM-YYYY), and timezone
def get_current_time():

    timezone = pytz.timezone("UTC")
    current_time = datetime.now(timezone)
    return current_time.strftime("%H:%M:%S"), current_time.strftime("%d-%m-%Y"), str(timezone)





# root agent definition
root_agent = Agent(
    name="tools_agent",
    model="gemini-2.5-flash-lite",
    description="adding up tools to the agents",
    instruction="""
    you are a helpful agent that can use tools to assist with tasks:
    get the current time, date, and timezone using the get_current_time tool.
    """,

    tools=[get_current_time],
)