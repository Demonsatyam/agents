# Tools Agent with Google ADK

This project demonstrates how to create a **basic AI agent** using the `google.adk` package and integrate it with custom tools.  
The agent can return the **current time**, **date** (DD-MM-YYYY), and **timezone** using Python’s `datetime` and `pytz` libraries.

---

## 📂 Project Structure

.
├── init.py # Marks the directory as a Python package
├── .env # Environment variables (API keys, configs)
└── agent.py # Core agent logic


---

## 🛠 Requirements

- **Python 3.8+**
- Install required packages:

```bash
pip install google-adk pytz


📜 How It Works
1️⃣ Importing Required Modules
from google.adk.agents import Agent
from google.adk.tools import google_search
from datetime import datetime
import pytz



Agent — Core class for defining an AI agent.

google_search — A built-in tool for performing Google searches (imported for possible extension).

datetime & pytz — Used to get and format time, date, and timezone.




2️⃣ Defining the Tool
def get_current_time():
    timezone = pytz.timezone("UTC")
    current_time = datetime.now(timezone)
    return current_time.strftime("%H:%M:%S"), current_time.strftime("%d-%m-%Y"), str(timezone)


This function returns:

Current Time in HH:MM:SS format

Current Date in DD-MM-YYYY format

Timezone as a string (UTC in this example)





3️⃣ Creating the Agent
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


name — Unique identifier for the agent.

model — AI model used for reasoning (gemini-2.5-flash-lite).

description — Short overview of the agent's role.

instruction — Prompt that guides the agent on how to use the tools.

tools — List of functions the agent can execute (in this case, only get_current_time).