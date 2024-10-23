import openai
from utils.secret_key import OPENAI_KEY
from utils.custom_logger import CustomLogger

client = openai.OpenAI(api_key=OPENAI_KEY)


def generate_from_code_assistant(persona, content, assistant, thread, name):
    """
    Clears all current thread but end, to preserve thread. Only used with coding_asssistant and coding_thread

    Args:

        Content: content (str)
        Name: name to show when logging

    Returns:
        Response: a list of the responses, in format {"role":"", "content":""}
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

    # Add persona and prompt
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",  # I want this to be system but it's only assistant or user. Could try putting it in assistant terms, e..g "I am a judge"..
        content=persona,
    )
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content,
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
        # Get the run steps - used to log code
        run_steps = client.beta.threads.runs.steps.list(
            thread_id=thread.id, run_id=run.id
        )
        run_steps_data = [step.model_dump() for step in run_steps.data]

        # Get all messages and turn into obj format
        thread_messages = client.beta.threads.messages.list(
            thread_id=thread.id, order="asc"
        )
        messages = []
        for message in thread_messages.data:
            content = ""
            for content_item in message.content:
                if hasattr(content_item, "text"):
                    content += content_item.text.value
            messages.append({"role": message.role, "content": content})

        CustomLogger.log_gpt(messages, f"{name} (code_assistant)")
        CustomLogger.log_code_interpreter(run_steps_data)

    # Dunno if this is needed
    else:
        print(f"weird run status: {run.status}")
        messages = []

    # ignore first 3 since they are dummy, persona, and prompt
    return messages[3:]
