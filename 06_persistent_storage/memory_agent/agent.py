from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Add a new reminder to the user's reminder list.

    Args:
        reminder: The reminder text to add
        tool_context: Context for accessing and updating session state

    Returns:
        A configuration message
    """
    print(f"--- Tools: add_reminder called for '{reminder}' ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Add the new reminder
    reminders.append(reminder)

    # Update state with the new list of reminders
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Reminder added: {reminder}"
    }


def view_reminders(tool_context: ToolContext) -> dict:
    """View all current reminders.


    Args:
        tool_context: Context for accessing session state

    Returns:
        The list of reminders
    """
    print("--- Tool: view_reminders called ---")

    # Get reminders from state
    reminders = tool_context.state.get("reminders", [])

    return {
        "action": "view_reminders",
        "reminders": reminders,
        "count": len(reminders)
    }


def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """Update an existing reminder.

    Args:
        index: The index of the reminder to update (1-based)
        updated_text: The new text for the reminder
        tool_context: Context for accessing and updating session state

    Returns:
        A configuration message
    """
    print(f"--- Tools: update_reminder called for index {index} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if 1 <= index <= len(reminders):
        # Update the reminder
        reminders[index - 1] = updated_text
        tool_context.state["reminders"] = reminders
        return {
            "action": "update_reminder",
            "index": index,
            "updated_text": updated_text,
            "message": f"Reminder updated: {updated_text}"
        }
    else:
        return {
            "action": "update_reminder",
            "index": index,
            "message": "Invalid reminder index"
        }
    

def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Delete an existing reminder.

    Args:
        index: The index of the reminder to delete (1-based)
        tool_context: Context for accessing and updating session state

    Returns:
        A configuration message
    """
    print(f"--- Tools: delete_reminder called for index {index} ---")

    # Get current reminders from state
    reminders = tool_context.state.get("reminders", [])

    # Check if the index is valid
    if 1 <= index <= len(reminders):
        # Delete the reminder
        deleted_reminder = reminders.pop(index - 1)
        tool_context.state["reminders"] = reminders
        return {
            "action": "delete_reminder",
            "index": index,
            "deleted_reminder": deleted_reminder,
            "message": f"Reminder deleted: {deleted_reminder}"
        }
    else:
        return {
            "action": "delete_reminder",
            "index": index,
            "message": "Invalid reminder index"
        }
    

def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A configuration message
    """
    print(f"--- Tools: update_user_name called for {name} ---")

    # Update the user's name in state
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "name": name,
        "message": f"User name updated: {name}"
    }




memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.5-flash-lite",
    description="A memory agent that remembers user preferences and answers frequently asked questions.",
    instruction="""

    You are a friendly reminder assistant that remembers users across conversations.

    The user's information is stored in state:
    - User's name: {user_name}
    - Reminders: {reminders}

    You can help the user manage with their reminders with the following capabilities:
    - Add a reminder
    - View existing reminders
    - Update a reminder
    - Delete a reminder
    - Update user name

    Always be friendly and address the user by their name. If you don't know their name,
    use the update_user_name tool to store it when they introduce themselves.

    **REMINDER MANAGEMENT GUIDELINES**

    When dealing with reminders, you need to be smart about finding the right reminders:

    1. When the user asks to update or delete a reminder but doesn't provide an idex:
       - If they mention the content of the reminder (e.g., "delete my meeting reminder"),
         look through the reminders to find a match

       - If you find an exact or close match, use that index
       - Never clarify which reminder the user is referring to, just use the first match
       - If no match is found, list all reminders and ask the user to specify

    2. When the user mentions a number or position:
       - Use that as the index (e.g., "delete reminder 2" means index=2)
       - Remember that indexing starts at 1 for the user

    3. For relative positions:
       - Handle "first", "last", "second", etc. appropriately
       - "First reminder" = index 1
       - "Last reminder" = the highest index
       - "Second reminder" = index 2, and so on

    4. For Viewing:
       - Always use the view_reminders tool when the user asks to see their reminders
       - Format the response in a numbered list for clarity
       - If there are no reminders, suggest adding some

    5. For addition:
       - Extract the actual reminder text from the user's request
       - Remove phrases like "add a reminder to" or "remind me to"
       - Focus on the task itself (e.g., "add a reminder to buy milk" -> add_reminder("buy milk"))

    6. For updates:
       - Identify both which reminder to update and what the new text should be
       - For example, "I've deleted your reminder to 'buy milk'"
    
    7. For deletions:
       - Confirm deletion when complete and mention which reminder was removed
       - For example, "I've deleted your reminder to 'buy milk'"

    Remember to explain that you can remember their information across conversation

    IMPORTANT:
    - use your best judgement to determine which reminder the user is refering to.
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which reminder they are referring to.
    """,

    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name
    ]
)