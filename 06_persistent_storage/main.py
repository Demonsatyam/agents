import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import call_agent_async
from memory_agent.agent import memory_agent


load_dotenv()

DB_URL = os.getenv("SESSION_DB_URL", "postgresql://satyam:8762@localhost:5432/session_db")
APP_NAME = "Memory Agent"
USER_ID = "satyam"

session_service = DatabaseSessionService(db_url=DB_URL)

initial_state = {
    "user_name": "Satyam",
    "reminders": [],
}

async def main_async():
    # Check for existing session
    existing = session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)

    if existing and len(existing.sessions) > 0:
        SESSION_ID = existing.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Create a new session with initial state
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    # Agent Runner Setup — do this for both new and existing sessions
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Interactive conversational loop
    print("\nWelcome to the Memory Agent!")
    print("Your reminders will be remembered across conversations")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the conversation. Goodbye!")
            break

        # Process the user query through the agent
        _ = await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

if __name__ == "__main__":
    asyncio.run(main_async())
