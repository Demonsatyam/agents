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
    ex
