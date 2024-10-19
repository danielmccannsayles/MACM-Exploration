import openai
from utils.secret_key import OPENAI_KEY


client = openai.OpenAI(api_key=OPENAI_KEY)


def generate_from_gpt(messages):
    """
    Messages:
        [{"role": "", "content": ""}, {"role": "", "content": ""}]"""
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
    )
    return response.choices[0].message.content


def generate_from_gpt_with_schema(messages, schema):
    """
    Return a response matching a schema (pydantic BaseModel)

    Messages:
        [{"role": "", "content": ""}, {"role": "", "content": ""}]
    """
    response = client.beta.chat.completions.parse(
        model="gpt-4o",  # To use schema we need to use gpt-4o
        messages=messages,
        response_format=schema,
    )
    return response.choices[0].message.parsed
