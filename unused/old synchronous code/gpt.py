import openai
from openai.types.chat import ChatCompletionMessage
from utils.secret_key import OPENAI_KEY
from pydantic import BaseModel
from utils.custom_logger import CustomLogger

client = openai.OpenAI(api_key=OPENAI_KEY)


def generate_from_gpt(messages: list[ChatCompletionMessage], title="Normal GPT"):
    """
    Messages:
        ChatCompletionMessage ([{"role": "", "content": ""}, {"role": "", "content": ""}])
    """
    response = client.chat.completions.create(
        model="gpt-4o",  # Trying out gpt-4o here to lower costs..
        messages=messages,
    )
    content = response.choices[0].message.content

    mlogs = messages
    mlogs.append({"role": "assistant", "content": content})
    CustomLogger.log_gpt(mlogs, title)

    return content


def generate_from_gpt_with_schema(
    messages: list[ChatCompletionMessage], schema: BaseModel, title="Schema GPT"
):
    """
    Return a response matching a schema (pydantic BaseModel)

    Messages:
        ChatCompletionMessage ([{"role": "", "content": ""}, {"role": "", "content": ""}])
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o",  # To use schema we need to use gpt-4o
        messages=messages,
        response_format=schema,
    )

    parsed = response.choices[0].message.parsed

    mlogs = messages
    mlogs.append({"role": "assistant", "content": parsed})
    CustomLogger.log_gpt(mlogs, title)

    return parsed
