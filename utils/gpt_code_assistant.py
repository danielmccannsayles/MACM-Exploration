import openai
from utils.secret_key import OPENAI_KEY
from utils.helpers import log_messages

client = openai.OpenAI(api_key=OPENAI_KEY)


def generate_from_code_assistant(persona, prompts, assistant, thread, name):
    """TODO: Consolidate persona and prompts somehow. Currently persona is ~ what used to be the assistant instructions

    Clears all current thread but end, to preserve thread. Only used with coding_asssistant and coding_thread

    Args:

        Prompts: list of prompts to handle - if multiple retains context. of form [{"role":"", "content": ""}]
        Name: name to show when logging

    Returns:
        Response: response from assistant
    """

    # Delete all messages but the prompt/chronologically first one - this will retain
    thread_messages = client.beta.threads.messages.list(thread.id)
    message_list = [message.model_dump() for message in thread_messages.data]

    for message in message_list[:-1]:
        id = message.get("id")

        client.beta.threads.messages.delete(
            message_id=id,
            thread_id=thread.id,
        )

    # TODO: Consolidate this w/ prompts somehow
    # Add the persona
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",  # I want this to be system but it's only assistant or user. Could try putting it in assistant terms, e..g "I am a judge"..
        content=persona,
    )

    # We can pass in multiple prompts if we want to retain context - make a run fo reach one
    for prompt in prompts:
        # Get the message and add it to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role=prompt["role"],
            content=prompt["content"],
        )

        # Start a new run - this is where we link the thread and the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # TODO: change this to handle streaming eventually, to stop blocking.. will have to see how code interp sessions work w/ it
        while run.status in ["queued", "in_progress"]:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == "completed":
            # Get message logs: all messages - for conversation, run steps - for tool calls
            all_messages = client.beta.threads.messages.list(thread_id=thread.id)
            run_steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id, run_id=run.id
            )
            run_steps_data = [step.model_dump() for step in run_steps.data]
            log_messages(all_messages, f"{name} (code_assistant)", run_steps_data)

            # Get response
            try:
                Assistant_response = all_messages.data[0].content[0].text.value
            except Exception as e:
                print(f"An error occurred: {e}")  # Avoid the image outputs
                Assistant_response = "I need to rethink this problem."
        else:
            print(f"weird run status: {run.status}")
            Assistant_response = "I need to rethink this problem"

    return Assistant_response
