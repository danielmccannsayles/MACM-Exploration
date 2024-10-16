def log_messages(messages, title, run_steps):
    """Function to format OpenAI thread messages as 'role: content', then add them to a log file

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
