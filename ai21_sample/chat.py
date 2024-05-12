import os
from dotenv import load_dotenv
import requests

load_dotenv()

ai_key = os.environ.get("AI21_API_KEY")

url = "https://api.ai21.com/studio/v1/j2-ultra/chat"

payload = {
    "numResults": 1,
    "temperature": 0.7,
    "messages": [
        {
            "text": "I'm crafting a market analysis tool for fintech leaders. How should I initiate the process?",
            "role": "user"
        },
        {
            "text": "1. Identify the target audience: Clearly define the fintech leaders who will benefit from the analysis tool. Consider factors such as industry, company size, and job function.\n2. Define the purpose of the tool: Define the key objectives of the market analysis tool, such as identifying market trends, assessing competition, or evaluating potential new markets.\n3. Determine the data sources: Identify the data sources that will be used to generate the analysis, such as market research reports, industry publications, and financial data.\n4. Design the user interface: Determine the layout of the user interface, including the types of charts and graphs that should be included, and the placement of key information.\n5. Test and refine the tool: Conduct user testing to ensure that the tool is easy to use and provides valuable insights. Make any necessary adjustments based on feedback.",
            "role": "assistant"
        },
        {
            "text": "Can you elaborate on the second item?",
            "role": "user"
        }
    ],
    "system": "You are an AI assistant for business research. Your responses should be informative and concise."

}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {ai_key}"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
