import json
import os

import openai
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

GPT_MODEL = os.getenv("MODEL_CONFIG_DEPLOYMENT")


# Refer: https://rapidapi.com/dickyagustin/api/text-translator2/details
def translate(text):
    url = "https://text-translator2.p.rapidapi.com/translate"

    payload = {
        "source_language": "en",
        "target_language": "vi",
        "text": text
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    body = response.json()
    if body["status"] == "success":
        return body["data"]["translatedText"]
    else:
        return "can not translate"


# Refer: https://rapidapi.com/visual-crossing-corporation-visual-crossing-corporation-default/api/visual-crossing-weather
def get_weather(location):
    url = "https://visual-crossing-weather.p.rapidapi.com/forecast"

    querystring = {"aggregateHours": "24", "location": location, "contentType": "json", "unitGroup": "us",
                   "shortColumnNames": "0"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        return "Can not get weather"
    data = response.json()
    return data["locations"][location]["values"][0]


def load_config():
    load_dotenv(dotenv_path=".env", override=True, verbose=True)
    openai.api_type = "azure"
    openai.api_key = os.getenv("MODEL_CONFIG_KEY")
    openai.api_base = os.getenv("MODEL_CONFIG_BASE")
    openai.api_version = os.getenv("MODEL_CONFIG_VERSION")


# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call="none", model=GPT_MODEL):
    try:
        response = openai.ChatCompletion.create(
            deployment_id=model,
            messages=messages,
            functions=functions,
            function_call=function_call
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))


def execute_function_call(message):
    function_name = message["function_call"]["name"]
    if function_name == "translate":
        query = json.loads(message["function_call"]["arguments"])["text"]
        results = translate(query)
    elif function_name == "get_current_weather":
        location = json.loads(message["function_call"]["arguments"])["location"]
        results = get_weather(location)
    else:
        results = "Function not found"
    return results


class GetCurrentWeather(BaseModel):
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


class Translate(BaseModel):
    text: str = Field(..., description="The text to translate")


def main():
    load_config()
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": GetCurrentWeather.model_json_schema(),
        },
        {
            "name": "translate",
            "description": "Translate from English to Vietnamese",
            "parameters": Translate.model_json_schema(),
        },
    ]

    messages = []
    messages.append({"role": "system",
                     "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
    messages.append({"role": "user",
                     "content": "Translate 'How are you' to Vietnamese"})
    chat_response = chat_completion_request(
        messages, functions=functions, function_call="auto"
    )
    assistant_message = chat_response["choices"][0]["message"]
    messages.append(assistant_message)
    if assistant_message.get("function_call"):
        results = execute_function_call(assistant_message)
        messages.append({"role": "function", "name": assistant_message["function_call"]["name"], "content": results})
    pretty_print_conversation(messages)


if __name__ == "__main__":
    main()
