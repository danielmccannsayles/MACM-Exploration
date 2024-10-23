import openai
from utils.secret_key import OPENAI_KEY


client = openai.OpenAI(api_key=OPENAI_KEY)


def create_agents_and_thread():
    coding_assistant = client.beta.assistants.create(
        model="gpt-4o",  # Let's try making this 4o. It should be much cheaper
        instructions="""You are a coding assistant. You *must* use the code interpreter to help solve the question""",
        name="Expert Coder",
        tools=[{"type": "code_interpreter"}],
    )

    coding_thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Take on the given role and answer the users question step by step",
            },
        ],
    )

    return (coding_assistant, coding_thread)
