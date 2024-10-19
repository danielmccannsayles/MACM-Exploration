def log_messages(messages, title, run_steps):
    """Function to format OpenAI thread messages as 'role: content', then add them to a log file

    Parameters:
    messages (object): role and content
    title (str): The name to prefix that chunk of messages
    run_steps(object): The run steps. Where tool calling is recorded

    Prints out messages in form -
    ====
    ## title
    ### role:
    content
    ===

    """

    ### Turn message obj into formatted strings
    all_messages = ["=======", f"## {title}"]
    for m in messages:
        role = m.get("role", "role")
        content = m.get("content", "content")
        all_messages.append(f"### {role}: \n{content}")

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
