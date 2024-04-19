import os
from openai import OpenAI
from dotenv import load_dotenv

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
        return response_text
    else:
        print("Failed to receive a valid response from GPT.")
        return "No response or invalid response from GPT."


