#!/usr/bin/env python3
from utils import print_yaml_highlighted
from gmail import get_unread_emails,  mark_email_as_read
from gpt import review
import json
import os
from settings import OPENAI_API_KEY

if not os.path.exists('credentials.json'):
    print("Hi, this sample script needs a credentials to a Gmail app created in the Google cloud console. Place the credentials aa ")
    print("https://console.cloud.google.com/marketplace/product/google/gmail.googleapis.com?q=search&referrer=search&project=famgpt-433416")
    exit(-1)


if OPENAI_API_KEY is None:
    print("Add your OpenAI to settings.py")
    exit(-1)

emails_tuples = []
prompt  = f"""
Extract the information from the email:
%s

Ignore label generic promotional emails as no-important. Label personal emails as important.

"""

# First loop to load from gmail
for email, msg_id, sender, gmail_message in get_unread_emails():
    full_prompt = prompt % (email,)
    py_response =  review(full_prompt, system="You are a helpful assistant processing emails")
    response = json.loads(py_response.json())
    print_yaml_highlighted(response)
    input()
