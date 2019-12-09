# GmailCLI
A gmail command line client made in Python

This is a command line tool for Gmail. It allows the user to send emails (with attachments) and read recent messages. Below is how to use it.

To use the tool, gmail authentication must first be established. Navigate to https://developers.google.com/gmail/api/quickstart/python and click “Enable the Gmail API”. You will need to download credentials.json. Make sure that this file downloads into the directory where gmailCLI.py is located. Now change the email variable in main() in gmailCLI.py to your own and save. Now we can run the tool. From the command line, cd into the directory where the files are located. See below for commands to run:

- Send  basic email:
  `python3 gmailCLI.py –send [receiver’s email] [Subject in quotes] [Body in quotes]`
  Example: `python3 gmailCLI.py -send receiver@gmail.com "Hello!" "This is a test"`
- Send email with attachment:
  `python3 gmailCLI.py –send [receiver’s email] [Subject in quotes] [Body in quotes] –a [file path]`
  Example: `python3 gmailCLI.py -send receiver@gmail.com "Test Picture" "Here is a cool pic" -a logo.jpg`
- Create basic draft:
  `python3 gmailCLI.py –draft [receiver’s email] [Subject in quotes] [Body in quotes]`
  Example: `python3 gmailCLI.py -draft receiver@gmail.com "CIS191 Question" "When is the final?"`
- Create draft with attachment:
  `python3 gmailCLI.py –draft [receiver’s email] [Subject in quotes] [Body in quotes] –a [file path]`
  Example: `python3 gmailCLI.py -draft receiver@gmail.com "Test Picture" "Here is a cool pic" -a logo.jpg`
- View n most recent emails:
  `python3 gmailCLI.py –get [number to fetch]`
  Example: `python3 gmailCLI.py –get 5`
