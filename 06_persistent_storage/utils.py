from turtle import _Color
from google.genai import types

class display_state:
    def __init__(self, session_service, app_name, user_id, session_id, message):
        self.session_service = session_service
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id
        self.message = message

async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{_Color.BG_RED}{_Color.WHITE}{_Color.BOLD} User Query: {query} {_Color.RESET}"
    )
    final_response_text = None


    # Display state before processing
    display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State before processing the query",
    )


    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            
            # Process each event ansd get the final response if available
            response = await process_agent_response(event)
            if response:
                final_response_text = response
            

        
    except Exception as e:
        print(f"Error during agent processing: {e}")
        

async def process_agent_response(event):
    """Process and display agent response events."""
    # Log basic event information
    print(f"Event ID: {event.id}, Author: {event.author}")
          
    # Check for the specific parts first
    has_specific_parts = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "executable code") and part.executable_code:
                # access the actual code string via .code
                print(
                    f" Debug: Agent generated code:\n```{part.executable_code.code}\n```"
                )
                has_specific_parts = True
            elif hasattr(part, "code_excution_result") and part.code_excution_result:
                # print tool response information
                print(
                    f" Tool Response: {part.tool_response.output}"
                )
                has_specific_parts = True

            # also print any text parts found in any event for debugging
            elif hasattr(part, "text") and part.text and part.text.isspace():
                print(f" Text: '{part.text.strip()}")


        # Check for a final response after specific parts
        final_response = None
        if event.is_final_response():
            if(
                event.content
                and event.content.parts
                and hasattr(event.content.parts[0], "text")
                and event.content.parts[0].text
            ):
                final_response = event.content.parts[0].text.strip()
                # use colors and formatting to make the final reponse stand out
                print(
                    # agent response
                    f"\n{_Color.BR_BLUE}{_Color.WHITE}{_Color.BOLD} Final Response: {final_response} {_Color.RESET}"
                )

                print(
                    f"\n{_Color.CYAN}{_Color.BOLD} Final Response: {final_response} {_Color.RESET}"
                )
                print(
                    f"\n{_Color.BG_BLUE}{_Color.WHITE}{_Color.BOLD} Final Response: {final_response} {_Color.RESET}"
                )
            else:
                print(
                    f"\n{_Color.BG_RED}{_Color.WHITE}{_Color.BOLD} No final response text found in event {_Color.RESET}"
                )