import openai
from utils.secret_key import OPENAI_KEY

client = openai.OpenAI(api_key=OPENAI_KEY)


# I'm not seeing why thinker has to be an assistant - doesn't look like it is even using the code interpreter
# Let's see if they're actually using code
def generate_from_thinker(
    prompts, max_tokens, model="gpt-4-1106-preview", temperature=0.7, n=1
):
    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You are a thinker. I need you to help me think about some problems.
        You need to provide me the answer based on the format of the example. If you use the code interpreter, 
        make sure to ALWAYS print() the final answer """,
        name="Thinker",
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()
    for i in range(len(prompts)):
        message = prompts[i]["content"]

        thread_message = client.beta.threads.messages.create(
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
                log_messages(all_messages, "Thinker", run_steps_data)

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


def generate_from_judge(
    prompts, max_tokens, model="gpt-4-1106-preview", temperature=0.7, n=1
):

    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You're a judge. I need you to make judgments on some statements. If you use the code interpreter, 
        make sure to ALWAYS print() the final answer""",
        name="Judge",
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()
    for i in range(len(prompts)):
        message = prompts[i]["content"]

        thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message,
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        while run.status in ["queued", "in_progress"]:
            # Retrieve the current run status
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            status = keep_retrieving_run.status

            # On complete, end & log messages
            if status == "completed":
                all_messages = client.beta.threads.messages.list(thread_id=thread.id)

                run_steps = client.beta.threads.runs.steps.list(
                    thread_id=thread.id, run_id=run.id
                )
                # Have to get data and then do this annoying thing
                run_steps_data = [step.model_dump() for step in run_steps.data]
                log_messages(all_messages, "Judge", run_steps_data)

                try:
                    Assistant_response = all_messages.data[0].content[0].text.value
                except Exception as e:
                    print(f"An error occurred: {e}")  # Avoid the image outputs
                    Assistant_response = "False"
                break

            elif status in ["queued", "in_progress"]:
                pass
            else:
                print(f"Run status: {keep_retrieving_run.status}")
                break
    return Assistant_response


def generate_from_excutor(
    prompts, max_tokens, model="gpt-4-1106-preview", temperature=0.7, n=1
):
    assistant = client.beta.assistants.create(
        model=model,
        instructions="""You're an excutor. I need you to calculate the final result based on some conditions and steps.
        You need to provide me the answer based on the format of the examples. If you use the code interpreter, 
        make sure to ALWAYS print() the final answer""",
        name="Excutor",
        tools=[{"type": "code_interpreter"}],
    )

    thread = client.beta.threads.create()
    for i in range(len(prompts)):
        message = prompts[i]["content"]

        thread_message = client.beta.threads.messages.create(
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
                log_messages(all_messages, "Executor", run_steps_data)

                try:
                    Assistant_response = all_messages.data[0].content[0].text.value
                except Exception as e:
                    print(f"An error occurred: {e}")  # Avoid the image outputs
                    Assistant_response = "False"
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


def log_messages(messages, title, run_steps):
    """
    Function to format OpenAI thread messages as 'role: content', then add them to a log file

    Parameters:
    messages (object): The messages object returned by OpenAI's threads API (in desc order, a.k.a reverse chronological)
    title (str): The name to prefix that chunk of messages
    run_steps(object): The run steps. Where tool calling is recorded

    Prints out messages in form -
    ====
    ## title
    ### role:
    content
    ===

    """

    ### Parse the messages
    # Check if the messages is correct, and reverse its order
    if messages and hasattr(messages, "data") and messages.data:
        raw_messages = messages.data  # Extract messages
        reversed_messages = raw_messages[::-1]  # Reverse the order
    else:
        print("No messages found or response is None")
        return

    all_messages = ["=======", f"## {title}"]
    # Iterate over messages and format them as 'role: content'
    for thread_message in reversed_messages:
        role = thread_message.role
        content = ""
        for content_item in thread_message.content:
            content += content_item.text.value

        formatted_message = f"### {role}: \n{content}"
        all_messages.append(formatted_message)

    ### Extract tool calls from the run_steps
    tool_calls = []
    for step in run_steps:
        if "tool_calls" in step["step_details"]:
            for tool_call in step["step_details"]["tool_calls"]:
                if tool_call.get("type") == "code_interpreter":
                    # Extract input and outputs
                    input = tool_call["code_interpreter"].get("input", "No input")
                    outputs = "\n".join(
                        [
                            output.get("logs", "")
                            for output in tool_call["code_interpreter"].get(
                                "outputs", []
                            )
                        ]
                    )
                    tool_calls.append(
                        f"Input: \n```\n{input}\n```\n \nOutputs: {outputs}"
                    )
    tool_call_string = "\n".join(tool_calls)

    # Add tool usage section to all_messages iff we have any tool usage
    tool_usage_section = f"### Tool Usage\n{tool_call_string}"
    if len(tool_calls) > 0:
        all_messages.append(tool_usage_section)

    # Join all messages with newlines
    parsed_messages = "\n".join(all_messages + ["======="])

    # Save to a file
    file_path = f"./output/messages.md"
    with open(file_path, "a") as f:
        # Write all messages to the file
        f.write(f"{parsed_messages}\n\n")
