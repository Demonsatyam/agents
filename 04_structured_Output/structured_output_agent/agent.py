from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


# define the class to return output_schema
class structured_output(BaseModel):
    subject: str = Field(
        description="The subject line of the email should be concise and relevant to the content of the email.",
    )
    body: str = Field(
        description="The main content of the email should be clear and provide all necessary information.",
    )




# root agent definition
root_agent = LlmAgent(
    name="structured_output_agent",
    model="gemini-2.5-flash-lite",
    description="an agent that generates structured output for emails",
    instruction="""

    You are a helpful mail generation agent that generates professional emails based on user request.
    The output should include a subject line and a body.
    IMPORTANT: YOU MUST RETURN THE OUTPUT IN THE JSON STRUCTURED FORMAT DEFINED BELOW.
    {
        "subject": "The subject line of the email",
        "body": "The main content of the email"
    }
    """,
    output_schema=structured_output,
    output_key="email",
)