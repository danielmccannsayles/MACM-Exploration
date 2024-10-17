import openai
import json
from utils.secret_key import OPENAI_KEY
from utils.helpers import log_messages

client = openai.OpenAI(api_key=OPENAI_KEY)


def test_gpt(assistant, thread, message):

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
            log_messages(
                all_messages, "test", run_steps_data
            )  # TODO: uncomment logging

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


def delete_messages(thread, dummy_id):
    thread_messages = client.beta.threads.messages.list(thread.id)
    message_list = [message.model_dump() for message in thread_messages.data]

    for message in message_list:
        id = message.get("id")

        # Avoid deleting dummy id
        if not id == dummy_id:
            client.beta.threads.messages.delete(
                message_id=id,
                thread_id=thread.id,
            )


## How can we keep the same thread while deleting things? Let's try adding a dummy thread message and deleting all others
## This dummy mesage works but it makes new sessions when its broken up by something not using the sessions
## Let's see if different assistants also cause it to make new sessions

assistant = client.beta.assistants.create(
    model="gpt-4o",
    instructions="""You are a coding assistant. Use the code interpreter and solve the question""",
    name="Test of Persistence",
    tools=[{"type": "code_interpreter"}],
)
# Start a thread w/ a dummy message
thread = client.beta.threads.create(
    messages=[
        {"role": "user", "content": "Please answer the following"},
        {"role": "user", "content": "Please answer the following"},
        {"role": "user", "content": "3rd"},
    ],
)

# Get the dummy message id
thread_messages = client.beta.threads.messages.list(thread.id)
message_list = [message.model_dump() for message in thread_messages.data]
dummy_id = message_list[0].get("id")


# Trying out second assistant - hopefully on diff thread won't interrupt
assistant_2 = client.beta.assistants.create(
    model="gpt-4o",
    instructions="""You are a coding assistant. Use the code interpreter and solve the question""",
    name="# 2",
)
# Start a thread w/ a dummy message
thread_2 = client.beta.threads.create(
    messages=[{"role": "user", "content": "Please answer the following"}],
)


#### First question
answer = test_gpt(
    assistant,
    thread,
    "Write a python program to calculate the first n fibonacci numbers. Check that it works by running it in the code interpreter, and print() out the final answer to make sure its actually correct.",
)

delete_messages(thread, dummy_id)

### Second question
answer = test_gpt(
    assistant,
    thread,
    "Write a python program to solve (x-2)/(x-3) for its roots. Check that it works by running it in the code interpreter, and print() out the final answer to make sure its actually correct.",
)

delete_messages(thread, dummy_id)

### Third question
answer = test_gpt(
    assistant_2,
    thread_2,
    "Whats a good joke?",
)

# delete_messages(thread, dummy_id)

### Fourth question
answer = test_gpt(
    assistant,
    thread,
    "Write a python program to count backwards from 100 to 0, only returning the even numbers. Check that it works by running it in the code interpreter, and print() out the final answer to make sure its actually correct.",
)

delete_messages(thread, dummy_id)

### I tried having this one not code - it seems like a switch between coding and not coding re-starts the session
### Fifth
# answer = test_gpt(
#     assistant,
#     thread,
#     "What is the meaning of life? Do NOT use the code interpreter",
# )

delete_messages(thread, dummy_id)

### Sixth
answer = test_gpt(
    assistant,
    thread,
    "Write a python program to calculate the square root of a number. Try it out with 1-10. Check that it works by running it in the code interpreter, and print() out the final answer to make sure its actually correct.",
)
