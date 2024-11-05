import os
import anyio


class AsyncLogger:
    """
    Instead of logging to files directly we save data until flush and then output it.
    """

    _log_directory = "./output/"
    _data: dict[str, str] = {}

    os.makedirs(_log_directory, exist_ok=True)

    @classmethod
    def clear_messages(self):
        self._data = {}

    @classmethod
    def add_message(self, path, *args):
        """Add message(s) to existing. Adds newline in between messages. Path can have multiple subdirs."""
        message = "\n".join([str(a) for a in args])
        if path in self._data:
            self._data[path] += f">> \n{message}"  # Add >> to make messages stand out
        else:
            self._data[path] = f">> {message}"

    @classmethod
    async def flush_one(self, path):
        """**ASYNC** Output one message. Clear message"""
        if path in self._data:
            intermediate_dirs = os.path.dirname(path)
            if intermediate_dirs:
                os.makedirs(f"{self._log_directory}{intermediate_dirs}", exist_ok=True)

            messages = self._data[path]
            async with await anyio.open_file(
                f"{self._log_directory}{path}.md", "w"
            ) as f:
                await f.write(messages)

            del self._data[path]

    @classmethod
    def flush(self):
        """Output all stored messages"""
        for path, messages in self._data.items():
            intermediate_dirs = os.path.dirname(path)
            if intermediate_dirs:
                os.makedirs(f"{self._log_directory}{intermediate_dirs}", exist_ok=True)

            with open(f"{self._log_directory}{path}.md", "w") as f:
                f.write(messages)

        self.clear_messages()
