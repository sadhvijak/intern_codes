from openai import OpenAI
import os
import openai
from dotenv import load_dotenv
import base64
import streamlit as st


from cryptography.fernet import Fernet
import json

# Load the encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()
        
    cipher_suite = Fernet(key)

    # Load the encrypted configuration data
    with open('config.json', 'r') as config_file:
        encrypted_data = json.load(config_file)

    # Decrypt the sensitive information
    # decrypted_data = {key: cipher_suite.decrypt(value.encode()).decode() for key, value in encrypted_data.items()}
    decrypted_data = {
        k: cipher_suite.decrypt(v.encode()).decode() 
        for k, v in encrypted_data.items()
    }
# print(data["API_KEY"])
api_key = decrypted_data.get("API_KEY")
print(f"🔑 Decrypted API Key: {api_key}")
client = OpenAI(api_key=api_key)

def get_answer(messages):
    system_message = [{"role": "system", "content": "You are an helpful AI chatbot, that answers questions asked by User."}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

# def text_to_speech(input_text):
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="nova",
#         input=input_text
#     )
#     webm_file_path = "temp_audio_play.mp3"
#     with open(webm_file_path, "wb") as f:
#         response.stream_to_file(webm_file_path)
#     return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
