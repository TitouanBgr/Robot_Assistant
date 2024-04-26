import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

def ask_to_gpt(transcribed_text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("No API key provided. Set OPENAI_API_KEY in your .env file.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant integrated into a robot system. Your role is to analyze and summerasize the text you have been receive."},
            {"role": "user", "content": transcribed_text}
        ]
    )

    if response and response.choices:
        response_text = response.choices[0].message.content
        send_to_discord_webhook(response_text)
        return response_text
    else:
        print("Failed to receive a valid response from GPT.")
        return "No response or invalid response from GPT."


def send_to_discord_webhook(content):
    headers = {'Content-Type': 'application/json'}
    current_time = datetime.utcnow().isoformat()
    data = {
        'embeds': [
            {
                "title": "MESSAGE PATIENT",
                "description": content, 
                "color": 5814783, 
                "fields": [],
                "footer": {
                    "text": "Robot Assistant - Système de gestion des soins"
                },
                "timestamp": current_time
            }
        ]
    }
    try:
        response = requests.post("https://discord.com/api/webhooks/1233381452083888188/efa8GPpDIo7yCBtUbcTtke724d_qWEX1vp3rN4Yx_nW_aKFo9mrtRDBPOgSkrYStJ-BA", headers=headers, json=data)
        return response.status_code == 204
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi du message : {e}")
        return False