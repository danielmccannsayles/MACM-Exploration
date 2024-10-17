import openai
from utils.secret_key import OPENAI_KEY


client = openai.OpenAI(api_key=OPENAI_KEY)


def create_agents_and_thread():
    thinker_assistant = client.beta.assistants.create(
        model="gpt-4-1106-preview",
        instructions="""You are a thinker. I need you to help me think about some problems.
        You need to provide me the answer based on the format of the example. """,
        name="Thinker",
    )

    executor_assistant = client.beta.assistants.create(
        model="gpt-4-1106-preview",
        instructions="""You're an excutor. I need you to calculate the final result based on some conditions and steps.
            You need to provide me the answer based on the format of the examples. """,
        name="Excutor",
    )

    judge_assistant = client.beta.assistants.create(
        model="gpt-4-1106-preview",
        instructions="""You're a judge. I need you to make judgments on some statements. """,
        name="Judge",
    )

    # I should be able to use just one thread since I'm clearing it each time:
    thread = client.beta.threads.create()

    coding_assistant = client.beta.assistants.create(
        model="gpt-4-1106-preview",
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

    return (
        (thinker_assistant, executor_assistant, judge_assistant),
        thread,
        (coding_assistant, coding_thread),
    )
