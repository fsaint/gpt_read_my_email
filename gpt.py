from openai import OpenAI
from settings import OPENAI_API_KEY
from datetime import datetime
from typing import Literal

from models import EmailAnalysis
client = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY,
)


def review(prompt, response_format = EmailAnalysis, system = None):
    try:
        response =  client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system", 
                    "content":  system
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-4o-mini",#gpt-4o-mini
            #tools=tools
            response_format=response_format
        )
        try:
            print("Tool Calls:", response.choices[0].message.tool_calls)
        except:
            print("Failed")
        #return response.choices[0].message.content
        print(f"Tokens used: {response.usage.total_tokens}")
        return response.choices[0].message.parsed
    except Exception as e:
        print(f"Error: {str(e)}")

