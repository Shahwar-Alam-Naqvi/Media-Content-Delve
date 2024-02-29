from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("MY_OPENAI_API_KEY"))

# Completion
def get_completion(messages,model="gpt-3.5-turbo",temperature=0,max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages = messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def generate_audio_from_text(text):
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input= text,
)
    return response.stream_to_file("output.mp3")

def get_image_url(feed_for_image):
    response = client.images.generate(
    model="dall-e-3",
    prompt=feed_for_image,
    size="1024x1024",
    quality="standard",
    n=1,    
    )

    image_url = response.data[0].url
    return image_url

def get_image_description(messages,model="gpt-4-vision-preview",temperature=0,max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages = messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content    