import os
from openai.types.chat import ChatCompletionMessage


# Uses Class methods to avoid creating an instance.
class CustomLogger:
    _current_file = "default"
    _log_directory = "./output/"

    # Make sure the log directory exists (at class init)
    os.makedirs(_log_directory, exist_ok=True)

    @classmethod
    def update_path(self, file_path):
        dirs_to_make = os.path.dirname(file_path)  # handle any intermediate dirs

        if dirs_to_make:
            os.makedirs(
                f"{self._log_directory}{dirs_to_make}", exist_ok=True
            )  # make intermediate directs
        self._current_file = file_path

    @classmethod
    def write_to_file(self, string):
        file_path = f"{self._log_directory}{self._current_file}.md"
        with open(file_path, "a") as f:
            f.write(string)

    @classmethod
    def default_log(self, title, *args):
        """Default logger - can be used for anything

        Prints:

        ====
        ## title
        arg
        arg
        ```
        """
        content = []
        for arg in args:
            content.append(str(arg))
        content_str = "\n".join(content)

        final_str = f"======\n## {title}\n {content_str} \n"
        self.write_to_file(final_str)

    @classmethod
    def log_gpt(self, messages: list[ChatCompletionMessage], title):
        """Log a call of messages in the form list[ChatCompletionMessage].

        Prints:
        ====
        ## title
        ### role:
        content
        ### role:
        content
        """
        all_messages = ["=======", f"## {title}"]
        for m in messages:
            role = m.get("role", "role")
            content = m.get("content", "content")
            all_messages.append(f"### {role}: \n{content}")

        final_str = "\n".join(all_messages)

        self.write_to_file(final_str)

    @classmethod
    def log_code_interpreter(self, run_steps):
        """Given run steps extract the code interpreter calls

        Prints:
        ### Code Interpreter
        Input:
        ```

        ```
        Outputs: (usually nothing)
        """
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

        # Return early if no tool calls were utilized
        if len(tool_calls) > 0:
            return

        tool_call_string = "\n".join(tool_calls)
        self.write_to_file(f"### Tool Usage\n{tool_call_string}")
