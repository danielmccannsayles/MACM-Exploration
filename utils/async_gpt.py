import openai
from openai.types.chat import ChatCompletionMessage
from utils.secret_key import OPENAI_KEY
from pydantic import BaseModel
import backoff
from openai import APIConnectionError

client = openai.AsyncOpenAI(api_key=OPENAI_KEY)


@backoff.on_exception(
    backoff.expo,  # Exponential backoff
    APIConnectionError,  # Retry on connection errors
    max_tries=5,  # Retry up to 5 times
    jitter=backoff.full_jitter,  # Add jitter to reduce likelihood of retry collisions
    on_backoff=lambda details: print(
        f"Retrying ({details['tries']} of {details['max_tries']}) due to {details['exception']}."
    ),
    on_giveup=lambda details: print(
        f"Failed after {details['tries']} attempts: {details['exception']}"
    ),
)
async def agenerate_from_gpt(messages: list[ChatCompletionMessage], title="Normal GPT"):
    """
    Messages:
        ChatCompletionMessage ([{"role": "", "content": ""}, {"role": "", "content": ""}])
    """
    response = await client.chat.completions.create(
        model="gpt-4o",  # Trying out gpt-4o here to lower costs..
        messages=messages,
    )
    return response.choices[0].message.content


@backoff.on_exception(
    backoff.expo,  # Exponential backoff
    APIConnectionError,  # Retry on connection errors
    max_tries=5,  # Retry up to 5 times
    jitter=backoff.full_jitter,  # Add jitter to reduce likelihood of retry collisions
    on_backoff=lambda details: print(
        f"Retrying ({details['tries']} of {details['max_tries']}) due to {details['exception']}."
    ),
    on_giveup=lambda details: print(
        f"Failed after {details['tries']} attempts: {details['exception']}"
    ),
)
async def agenerate_from_gpt_with_schema(
    messages: list[ChatCompletionMessage], schema: BaseModel, title="Schema GPT"
):
    """
    Return a response matching a schema (pydantic BaseModel)

    Messages:
        ChatCompletionMessage ([{"role": "", "content": ""}, {"role": "", "content": ""}])
    """
    response = await client.beta.chat.completions.parse(
        model="gpt-4o",  # To use schema we need to use gpt-4o
        messages=messages,
        response_format=schema,
    )

    return response.choices[0].message.parsed
