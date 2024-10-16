import openai
import json
from utils.secret_key import OPENAI_KEY
from utils.gpt_robots import log_messages

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
            # log_messages(all_messages, "test", run_steps_data) #TODO: uncomment logging

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


#### Testing out persistent threads
# New assistant
assistant = client.beta.assistants.create(
    model="gpt-4-1106-preview",
    instructions="""You are a coding assistant. Use the code interpreter and solve the question""",
    name="Test of Persistence",
    tools=[{"type": "code_interpreter"}],
)
# Start a thread
thread = client.beta.threads.create()


#### First question
answer = test_gpt(
    assistant,
    thread,
    "Write a python program to calculate the first n fibonacci numbers. Check that it works by running it in the code interpreter, and print() out the final answer to make sure its actually correct.",
)
thread_messages = client.beta.threads.messages.list(thread.id)
message_list = [message.model_dump() for message in thread_messages.data]
with open("./output/test.txt", "a") as f:
    f.write(json.dumps(message_list, indent=4))
    f.write("END \n\n\n")

### Lets try and delete all the messages
for message in message_list:
    id = message.get("id")
    print(id)

    client.beta.threads.messages.delete(
        message_id=id,
        thread_id=thread.id,
    )

### Second question
answer = test_gpt(
    assistant,
    thread,
    "Write a python program to solve (x-2)/(x-3) for its roots. Check that it works by running it in the code interpreter, and print() out the final answer to make sure its actually correct.",
)
thread_messages = client.beta.threads.messages.list(thread.id)
message_list = [message.model_dump() for message in thread_messages.data]
with open("./output/test.txt", "a") as f:
    f.write(json.dumps(message_list, indent=4))
    f.write("END \n\n\n")
