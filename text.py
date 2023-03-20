import requests
import key

def send_text(message):
  resp = requests.post('https://textbelt.com/text', {
    'phone': key.get_key,
    'message': message,
    'key': 'textbelt',
  })
  print(resp.json())