from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def send_message_to_ai(context):
    # Nachricht an die KI senden und Antwort zurückgeben
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=context
    )
    assistant_reply = response.choices[0].message.content
    return assistant_reply