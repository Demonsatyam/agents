import asyncio
import psycopg2
import os
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from dotenv import load_dotenv
from utils import call_agent_async

load_dotenv()
db_url = "postgresql://satyam:8762@localhost:5432/session_db"
session_service = DatabaseSessionService(db_url=db_url)

initial_state = {
    "user_name": "Satyam",
    "reminders": [],
}


async def main_async():
    # setup constants
    APP_NAME = "Memory Agent"
    USER_ID = "satyam"


    # check for existing session for this user
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # if there's an existing session, use it otherwise create a new one
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
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


        # Agent Runner Setup
        runner = Runner(
            agent="memory_agent",
            app_name=APP_NAME,
            session_service=session_service,
        )



        # Interactive conversational loop
        print("\nWelcome to the Memory Agent!")
        print("Your reminders will be remembered across conversations")
        print("Type 'exit' to end the conversation.\n")

        while True:
            # Get user input
            user_input = input("You: ")

            # Check if user wants to exit
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting the conversation. Goodbye!")
                break

            # Process the user query through the agent
            await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main_async())