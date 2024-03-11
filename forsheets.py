"""
Conversion of informal text to spreadsheet-oriented formula.

This module provides functions for generating and explaining spreadsheet formulas based on user input. It utilizes the OpenAI API
for natural language processing and model-driven responses.

Functions:
1. generate(user_input: str) -> Any:
   - Generates a spreadsheet formula from user input.
   - Uses the OpenAI GPT-3.5-turbo model for text-to-formula conversion.
   - Returns the generated formula as a JSON string.

2. lecture(user_input: str) -> Any:
   - Explains a given spreadsheet formula.
   - Uses the OpenAI GPT-3.5-turbo model to provide an explanation for the input formula.
   - Returns the explanation as a JSON string.

Note:
- The module uses the OpenAI API key, which should be provided as an environment variable named OPENAI_API_KEY.
- The OpenAI API key is loaded using the dotenv library from the .env file in the same directory as this module.

Example Usage:
```python
from forsheet import generate, lecture

# Generate a formula
user_input = "Add the values in cells A1 to A10"
formula = generate(user_input)
print(formula)

# Explain a formula
user_input = "=SUM(B2:B10)"
explanation = lecture(user_input)
print(explanation)

"""

import os
import json
from openai import OpenAI
from typing import Any
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate(user_input: str) -> Any:
    """
        Generate spreadsheet formula from user input.

        -   Extract Formula from JSON dump
        -   Send Text through Flask to JS
    """

    # Generate a formula
    response: json = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "AI powered text to formula generator that generates spreadsheet formula only from user input"},
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
    """
        Explain the Generated Formula
        -   Request explanation and extract response from JSON Dump
        -   Send Response Through Flask to JS
    """
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
