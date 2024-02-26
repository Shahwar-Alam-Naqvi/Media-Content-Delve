from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("MY_OPENAI_API_KEY"))

# Completion
def get_completion(messages,model="gpt-3.5-turbo",temperature=0,max_tokens=50):
    response = client.chat.completions.create(
        model=model,
        messages = messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

import openai

# def generate_audio_from_text(text):
#     response = openai.TextToSpeech.create(
#         text=text,
#         voice="voice_of_choice",
#     )

#     # Assuming the response has binary data for the audio file
#     with open('output_audio.mp3', 'wb') as audio_file:
#         audio_file.write(response.audio_content)

def generate_audio_from_text(text):
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input= text,
)
    return response.stream_to_file("output.mp3")