import os
from ai21 import AI21Client
from dotenv import load_dotenv
import requests


load_dotenv()

# Initialize the AI21Client with your API key
ai_key = os.environ.get("AI21_API_KEY")


url = "https://api.ai21.com/studio/v1/summarize"

payload = { 
           "source": "The winners of the Frontend Challenge: Earth Day Edition were announced, showcasing creative and skillful submissions. The challenge had prompts for CSS Art and Glam Up My Markup, with a special prize category for submissions that brought awareness to climate change. Another Frontend Challenge will be hosted soon.",
           "sourceType": "TEXT" ,
        }
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {ai_key}"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)