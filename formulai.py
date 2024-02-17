"""
Conversion of informal text to spreadsheet oriented formula
"""

import os
import json
from openai import OpenAI
from typing import Any
from dotenv import load_dotenv
from openai.types.chat import ChatCompletion

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate(user_input: str) -> Any:
    # Generate a formula
    response: json = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Strictly generate an spreadsheet formula from user input. Return 'invalid input' for bad input"},
            {"role": "user", "content": "{}".format(user_input)}
        ],
        temperature=0,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return json.dumps(response.choices[0].message.content)


def lecture(user_input):
    # Explain a formula
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Explain this spreadsheet formula"},
            {"role": "user", "content": "{}".format(user_input)}
        ],
        temperature=0,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return json.dumps(response.choices[0].message.content)

# Convert this to spreadsheet formula
