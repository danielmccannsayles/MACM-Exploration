import openai
from openai.types.chat import ChatCompletionMessage
from utils.secret_key import OPENAI_KEY
from pydantic import BaseModel
import backoff
from openai import APIConnectionError
import httpx

# Custom time out settings - hopefully to avoid all these errors
timeout_settings = httpx.Timeout(
    connect=5.0,  # seconds to wait for a connection to be established
    read=15.0,  # TODO: keep incrementing this to max 30sec if i keeps failing
    write=10.0,  # seconds to wait for data to be written to the connection
    pool=5.0,  # max time to wait for an available connection in the pool
)


client = openai.AsyncOpenAI(api_key=OPENAI_KEY, timeout=timeout_settings)


@backoff.on_exception(
    backoff.expo,  # Exponential backoff
    APIConnectionError,  # Retry on connection errors
    max_tries=5,  # Retry up to 5 times
    jitter=backoff.full_jitter,  # Add jitter to reduce likelihood of retry collisions
    on_backoff=lambda details: print(
        f"Retrying ({details.get('tries','n/a')} of {details.get('max_tries','n/a')}) due to {details.get('exception','n/a')}."
    ),
    on_giveup=lambda details: print(
        f"Failed after {details.get('tries', 'n/a')} attempts: {details.get('exception','n/a')}"
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
        f"Retrying ({details.get('tries','n/a')} of {details.get('max_tries','n/a')}) due to {details.get('exception','n/a')}."
    ),
    on_giveup=lambda details: print(
        f"Failed after {details.get('tries', 'n/a')} attempts: {details.get('exception','n/a')}"
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
