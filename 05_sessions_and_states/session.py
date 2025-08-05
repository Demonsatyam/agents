# import sys
# import os
# from dotenv import load_dotenv
# from google.adk.sessions import InMemorySessionService
# from google.adk.runners import Runner
# from google.genai import types
# import uuid
# from faq_agent import faq_agent

# load_dotenv()

# # create a session service to store state
# session_service_stateful = InMemorySessionService()

# initial_state = {
#     "user_id": "Satyam",
#     "user_preferences": """
#     - Language: en
#     - Age: 21
#     - Hobbies: [astronomy, coding, gaming, wildlife]
#     - Profession: student
#     - College: Chandigarh University
#     - Year of Graduation: 2026
#     - Interests: [AI, ML, Web Development, Cloud Computing]
#     """,
# }

# # create new session
# APP_NAME = "ExploreAI"
# USER_ID = "Satyam"
# SESSION_ID = str(uuid.uuid4())

# stateful_session = session_service_stateful.create_session(
#     app_name=APP_NAME,
#     user_id=USER_ID,
#     session_id=SESSION_ID,
#     state=initial_state,
# )

# print(f"Session created with ID: {stateful_session.id}")

# # runner that contains the agent, session service, and app name
# runner = Runner(
#     agent=faq_agent,
#     app_name=APP_NAME,
#     session_service=session_service_stateful,
# )

# # create a new message
# new_message = types.Content(
#     role="user",
#     parts=[types.Part(text="What is Satyam's favourite TV Show?")]
# )

# # run the agent
# # run the agent
# for event in runner.run(
#     user_id=USER_ID,
#     session_id=SESSION_ID,
#     input=new_message,  # ✅ use input instead of new_message
# ):
#     if event.final_response():
#         if event.content and event.content.text:
#             print(f"Final response: {event.content.parts[0].text}")


# # session event exploration
# print(f"\nSession Event Exploration")
# session = session_service_stateful.get_session(
#     app_name=APP_NAME,
#     user_id=USER_ID,
#     session_id=stateful_session.id,  # ✅ FIXED here too
# )

# # final session state
# print(f"\nFinal Session State")
# for key, value in session.state.items():
#     print(f"{key}: {value}")




import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from faq_agent import faq_agent

load_dotenv()



# Create a session service to store state
use_session_service = InMemorySessionService()


initial_state = {
    "user_name": "Satyam",
    "user_preferences": """
    I like to play Table Tennis, Cricket, and Basketball.
    I am a fan of the TV show 'The Big Bang Theory'.
    I enjoy watching wildlife documentaries.
    I am interested in AI, ML, Web Development, and Cloud Computing.
    I am a student at Chandigarh University, graduating in 2026.
    """
}



# Create new session
APP_NAME = "AI Bot"
USER_ID = "Satyam"
SESSION_ID = str(uuid.uuid4())
stateful_session = use_session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION: ")
print(f"\tSession ID: {SESSION_ID}")



runner = Runner(
    agent=faq_agent,
    app_name=APP_NAME,
    session_service=use_session_service,
)


new_message = types.Content(
    role="user", parts=[types.Part(text="What is Satyam's favourite TV show?")]
)



for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final response: {event.content.parts[0].text}")


print("==== Session Event Exploration ==== ")
session = use_session_service.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)



# Log final session state
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key}: {value}")
