import openai
import json
from utils.secret_key import OPENAI_KEY
from utils.gpt_robots import log_messages

client = openai.OpenAI(api_key=OPENAI_KEY)


def test_gpt(message, max_tokens, model="gpt-4-1106-preview", temperature=0.7, n=1):
    # Create a new assistant - shouldn't be done each time Idt - I think it makes a new code interpreter each time
    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You are a coding assistant. Use the code interpreter and solve the question""",
        name="Test",
        tools=[{"type": "code_interpreter"}],
    )

    # Start a thread
    thread = client.beta.threads.create()

    # Add the content: mesage here
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    while run.status in ["queued", "in_progress"]:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )

        if keep_retrieving_run.status == "completed":
            all_messages = client.beta.threads.messages.list(thread_id=thread.id)

            run_steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id, run_id=run.id
            )
            # Have to get data and then do this annoying thing
            run_steps_data = [step.model_dump() for step in run_steps.data]
            log_messages(all_messages, "test", run_steps_data)

            try:
                Assistant_response = all_messages.data[0].content[0].text.value
            except Exception as e:
                print(f"An error occurred: {e}")  # Avoid the image outputs
                Assistant_response = "I need to rethink this problem."
            break

        elif (
            keep_retrieving_run.status == "queued"
            or keep_retrieving_run.status == "in_progress"
        ):
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break
    return Assistant_response


answer = test_gpt(
    "Write a python program to calculate the first n fibonacci numbers. Check that it works by running it in the code interpreter, and print() out the final answer to make sure its actually correct.",
    max_tokens=256,
    model="gpt-4-1106-preview",
    temperature=0.7,
    n=1,
)
