import base64
import os.path
import time
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests



# Configuration OAuth 2.0 FOR CONFIGURE THIS GO TO CHAT GPT OR GOOGLE DOCUMENTATIONS
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# telegram var
token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('ID') #Telegram chat_id



def authenticate():
    creds = None
    # Charger les informations d'identification
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Si les informations d'identification n'existent pas ou ont expiré, demander une nouvelle autorisation
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Sauvegarder les informations d'identification pour les utilisations futures
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

def search_emails(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])
    return messages

def get_email(service, email_id):
    message = service.users().messages().get(userId='me', id=email_id, format='full').execute()
    return message

def mark_as_archived(service, email_id):
    service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['INBOX']}).execute()

# update: Update, context: CallbackContext    
def send_telegram():
  msg = f"\n{mail_sender} \n\n {sujet} \n\n {body}"
  msg_tmp = msg.replace('(', '').replace(')', '').replace(':', '').replace(',', '').replace("'", "")
  msg_final = f'🔥🔥🔥 MAIL ALERT 🔥🔥🔥\n {msg_tmp}'
  
  message = ('https://api.telegram.org/bot'+ token + '/sendMessage?chat_id=' + chat_id + '&text=' + msg_final)
  requests.post(message)

  
  
  
# Authentification avec OAuth 2.0
creds = authenticate()
service = build('gmail', 'v1', credentials=creds)

# Rechercher les e-mails contenant le mot TRIGGER dans la boîte de réception uniquement
query = 'wölkli in:inbox'
messages = search_emails(service, query)

query2 = 'TEST in:inbox'
messages2 = search_emails(service, query2)

query3 = 'GitHub in:inbox'
messages3 = search_emails(service, query3)



# Afficher le contenu des e-mails du Nextcloud
for message in messages:
    email = get_email(service, message['id'])
    body = email['snippet']
    mail_sender = email['payload']['headers'][17]['value']
    sujet = email['payload']['headers'][19]['value']
    
  
    print('ID:', email['id'])
    print('From : ', mail_sender)  # Affiche l'expéditeur
    print('Sujet : ', sujet)  # Affiche le sujet
    print('Body:', body)
    print('---')
    send_telegram()
    mark_as_archived(service, email['id'])
    
    
    
# Afficher le contenu des e-mails de TEST
for message in messages2:
    email = get_email(service, message['id'])
    body = email['snippet']
    mail_sender = email['payload']['headers'][17]['value']
    sujet = email['payload']['headers'][19]['value']
    
  
    print('ID:', email['id'])
    print('From : ', mail_sender)  # Affiche l'expéditeur
    print('Sujet : ', sujet)  # Affiche le sujet
    print('Body:', body)
    print('---')
    send_telegram()
    mark_as_archived(service, email['id'])
    
# Afficher le contenu des e-mails GITHUB
for message in messages3:
    email = get_email(service, message['id'])
    body = email['snippet']
    mail_sender = email['payload']['headers'][17]['value']
    sujet = email['payload']['headers'][19]['value']
    
  
    print('ID:', email['id'])
    print('From : ', mail_sender)  # Affiche l'expéditeur
    print('Sujet : ', sujet)  # Affiche le sujet
    print('Body:', body)
    print('---')
    send_telegram()
    mark_as_archived(service, email['id'])

