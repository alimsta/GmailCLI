from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import base64
import mimetypes
import email

import argparse

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-draft', nargs=3, required=False)
    parser.add_argument('-send', nargs=3, required=False)
    parser.add_argument('-a', nargs=1, required=False)
    parser.add_argument('-get', nargs=1, required=False)

    args = parser.parse_args()
    email = '' #Change to your own email.
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('gmail', 'v1', credentials=creds)

    if args.send is not None:
        if args.a is None:
            msg = create_message(email, args.send[0], args.send[1], args.send[2])
            send_message(service, 'me', msg)
        else:
            msg = create_message_with_attachment(email, args.send[0], args.send[1], args.send[2], args.a[0])
            send_message(service, 'me', msg)
    elif args.get is not None:
        get_messages(service, args.get[0])
    elif args.draft is not None:
        if args.a is None:
            msg = create_message(email, args.draft[0], args.draft[1], args.draft[2])
            create_draft(service, 'me', msg)
        else:
            msg = create_message_with_attachment(email, args.draft[0], args.draft[1], args.draft[2], args.a[0])
            create_draft(service, 'me', msg)

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_message.decode()}

def create_message_with_attachment(sender, to, subject, message_text, file):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    
    main_type, sub_type = content_type.split('/', 1)

    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    encoded_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_message.decode()}

def create_draft(service, user_id, message_body):
    """Create and insert a draft email. Print the returned draft's message and id.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

    Returns:
    Draft object, including draft id and message meta data.
    """
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        print('Draft Id: %s' % draft['id'])
        return draft
    except:
        print('An error occurred')
        return None

def send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
     Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
        print('Message Id: %s' % message['id'])
        return message
    except:
        print('An error occurred')

def get_messages(service, n):
    msgs = service.users().messages().list(userId='me', maxResults=n).execute()
    for i in msgs['messages']:
        message = service.users().messages().get(userId='me', id=i['id']).execute()
        for h in message['payload']['headers']:
            if h['name'] == 'Date':
                print('Date: '+h['value'])
            if h['name'] == 'From':
                print('From: '+h['value'])
            if h['name'] == 'Subject':
                print('Subject: '+h['value'])
        print(message['snippet'])
        print()  

if __name__ == '__main__':
    main()
