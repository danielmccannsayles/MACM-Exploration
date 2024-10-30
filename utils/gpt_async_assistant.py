import openai
from utils.secret_key import OPENAI_KEY

client = openai.AsyncOpenAI(api_key=OPENAI_KEY)


async def agenerate_from_code_assistant(persona, content, assistant, thread):
    """
    ASYNC
    Clears all current thread but end, to preserve thread. Only used with coding_asssistant and coding_thread

    Args:
        Content: content (str)
        Name: name to show when logging

    Returns:
        Response: a list of the responses, in format {"role":"", "content":""}
    """

    # Delete all messages but the dummy - the chronologically first one - this will retain code sessions
    thread_messages = await client.beta.threads.messages.list(thread.id)
    message_list = [message.model_dump() for message in thread_messages.data]
    for message in message_list[:-1]:
        id = message.get("id")
        await client.beta.threads.messages.delete(
            message_id=id,
            thread_id=thread.id,
        )

    # Add persona and prompt messages
    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",  # I want this to be system but it's only assistant or user. Could try putting it in assistant terms, e..g "I am a judge"..
        content=persona,
    )
    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content,
    )

    # Start a new run - this is where we link the thread and the assistant
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status in ["queued", "in_progress"]:
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )

    if run.status == "completed":
        # Get all messages and turn into obj format
        thread_messages = await client.beta.threads.messages.list(
            thread_id=thread.id, order="asc"
        )
        messages = []
        for message in thread_messages.data:
            content = ""
            for content_item in message.content:
                if hasattr(content_item, "text"):
                    content += content_item.text.value
            messages.append({"role": message.role, "content": content})

    else:
        print(f"weird run status: {run.status}")
        messages = []

    # ignore first 3 since they are dummy, persona, and prompt
    return messages[3:]
