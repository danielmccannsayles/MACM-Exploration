import openai
from utils.secret_key import OPENAI_KEY
from utils.helpers import log_messages

client = openai.OpenAI(api_key=OPENAI_KEY)


def create_agents_and_thread():
    thinker_assistant = client.beta.assistants.create(
        model="gpt-4-1106-preview",
        instructions="""You are a thinker. I need you to help me think about some problems.
        You need to provide me the answer based on the format of the example. """,
        name="Thinker",
        tools=[{"type": "code_interpreter"}],
    )

    executor_assistant = client.beta.assistants.create(
        model="gpt-4-1106-preview",
        instructions="""You're an excutor. I need you to calculate the final result based on some conditions and steps.
            You need to provide me the answer based on the format of the examples. """,
        name="Excutor",
        tools=[{"type": "code_interpreter"}],
    )

    judge_assistant = client.beta.assistants.create(
        model="gpt-4-1106-preview",
        instructions="""You're a judge. I need you to make judgments on some statements. """,
        name="Judge",
        tools=[{"type": "code_interpreter"}],
    )

    # I should be able to use just one thread since I'm clearing it each time:
    thread = client.beta.threads.create()
    return thinker_assistant, executor_assistant, judge_assistant, thread


def generate_from_assistant(prompts, assistant, thread, name):
    """Clears current thread, generates new responses based on prompt(s) passed. Does not handle thread timeout (yet?)

    Args:
        Prompts: list of prompts to handle - if multiple retains context
        Name: name to show when logging

    Returns:
        Response: response from assistant
    """

    # Clear the thread messages - costs nothing and AVOIDS making a new thread/code interpreter session :)
    # First get messages, then format, then go through and call .delete() with the message id
    thread_messages = client.beta.threads.messages.list(thread.id)
    message_list = [message.model_dump() for message in thread_messages.data]

    for message in message_list:
        id = message.get("id")
        client.beta.threads.messages.delete(
            message_id=id,
            thread_id=thread.id,
        )

    # We can pass in multiple prompts if we want to retain context
    for prompt in prompts:
        # Get the message and add it to the thread
        message = prompt["content"]
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        )

        # Start a new run - this is where we link the thread and the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # TODO: consolidate keep retriving and run into one variable. Check out polling from docs
        while run.status in ["queued", "in_progress"]:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )

            if keep_retrieving_run.status == "completed":
                # Get message logs: all messages - for conversation, run steps - for tool calls
                all_messages = client.beta.threads.messages.list(thread_id=thread.id)
                run_steps = client.beta.threads.runs.steps.list(
                    thread_id=thread.id, run_id=run.id
                )
                run_steps_data = [step.model_dump() for step in run_steps.data]
                log_messages(all_messages, name, run_steps_data)

                # Get response
                try:
                    Assistant_response = all_messages.data[0].content[0].text.value
                except Exception as e:
                    print(f"An error occurred: {e}")  # Avoid the image outputs
                    Assistant_response = "I need to rethink this problem."
                break

            # TODO: remove this in favor of actually using the while loop LOL
            elif (
                keep_retrieving_run.status == "queued"
                or keep_retrieving_run.status == "in_progress"
            ):
                pass
            else:
                print(f"Run status: {keep_retrieving_run.status}")
                break
    return Assistant_response
