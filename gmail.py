import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# If modifying these SCOPES, delete the file token.json.
SCOPES = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/tasks'
]

import base64

def remove_empty_lines(text):
    """Remove empty lines from the given text."""
    # Split the text into lines, filter out empty lines, and join back into a single string
    cleaned_text = "\n".join(line for line in text.splitlines() if line.strip())
    return cleaned_text

def get_email_content(message):
    """Extracts the email content from a Gmail message object."""
    email_data = {}

    # Extract headers for important information
    headers = message['payload']['headers']
    for header in headers:
        if header['name'].lower() == 'from':
            email_data['From'] = header['value']
        elif header['name'].lower() == 'subject':
            email_data['Subject'] = header['value']
        elif header['name'].lower() == 'date':
            email_data['Date'] = header['value']

    # Extract the body of the email
    email_data['Body'] = extract_body(message['payload'])

    email_content = ''
    # Combine the extracted information into a single string
    #if 'From' in email_data:
    email_content += f"From: {email_data['From']}\n"
    email_content += f"Subject: {email_data['Subject']}\n"
    email_content += f"Date: {email_data.get('Date')}\n\n"
    email_content += email_data['Body']

    return remove_empty_lines(email_content)

def extract_body(payload):
    """Recursively extract the body of the email from the payload."""
    body = ''

    if 'parts' in payload:
        for part in payload['parts']:
            body += extract_body(part)
    elif 'body' in payload and 'data' in payload['body']:
        data = payload['body']['data']
        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
        body += decoded_data

    return body

def authenticate_gmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_unread_emails(frm = None, unread = True):
    # Call the Gmail API
    #from:@example.com
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    q = ""
    if unread:
        q = "is:unread"
    if frm:
        domains = '@mcds.org', '@mcds.myenotice.com', '@sterneschool.org', '@c5children.org'
        domain_q = " OR ".join(domains)
        domain_q = " from: ({%s})" % domain_q
        q = q +  domain_q
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=q).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print('No new messages.')
        return
    
    print(f'You have {len(messages)} unread messages.')
    
    for msg in messages:
        msg = service.users().messages().get(userId='me', id=msg['id']).execute()
        print([x['value'] for x in msg['payload']['headers'] if x['name'] in ['From','Date']])
        email_content = get_email_content(msg)
        yield email_content, msg['id'], [x['value'] for x in msg['payload']['headers'] if x['name'].lower() == 'from'][0], msg

def get_credentials():
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds



def mark_email_as_read(message_id=None, user_id='me'):
    creds =  get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    if message_id:
        try:
            # Modify the message labels to remove 'UNREAD'
            service.users().messages().modify(
                userId=user_id,
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            print(f"Email with ID {message_id} marked as read.")
        except Exception as error:
            print(f"An error occurred: {error}")
    else:
        print("No message ID provided.")



def archive_email(msg_id, user_id = 'me'):
    """Archive an email by removing the INBOX label."""
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    try:
        # Remove the 'INBOX' label to archive the email
        service.users().messages().modify(
            userId=user_id,
            id=msg_id,
            body={
                'removeLabelIds': ['INBOX'],
                'addLabelIds': []
            }
        ).execute()
        print(f"Email with ID {msg_id} has been archived.")
    except Exception as error:
        print(f"An error occurred: {error}")

