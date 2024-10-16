# All my assistants are cluttering things up. Run this to delete them (100 of them) and make it cleaner

import openai
from utils.secret_key import OPENAI_KEY

client = openai.OpenAI(api_key=OPENAI_KEY)

# Get assistants, manhandle them into dicts, go through and delete them using their id
my_assistants = client.beta.assistants.list(
    order="desc",
    limit="100",
)
assistant_list = [assistant.model_dump() for assistant in my_assistants.data]
print(f"{len(assistant_list)} assistants found")

for i, assistant in enumerate(assistant_list):
    id = assistant.get("id")
    client.beta.assistants.delete(id)
    print(f"Deleted {i} assistant(s)", end="\r")

# Check if any are remaining
my_assistants = client.beta.assistants.list(
    order="desc",
    limit="100",
)
assistant_list = [assistant.model_dump() for assistant in my_assistants.data]
print(f"{len(assistant_list)} assistants remaining")
