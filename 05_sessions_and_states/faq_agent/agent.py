from google.adk.agents import Agent


faq_agent = Agent(
    name="faq_agent",
    model="gemini-2.5-flash-lite",
    description="An agent that answers frequently asked questions.",
    instruction="""
    You are an agent designed to answer frequently asked questions.
    here are some information about the user:

    Name:
    {user_name}
    Preferences:
    {user_preferences}
    """,
)