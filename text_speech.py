import openai
from gtts import gTTS
import os
import streamlit as st
import base64

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a response from OpenAI GPT
def get_llm_response(messages, model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# Function to convert text to speech using gTTS
def text_to_speech(text):
    tts = gTTS(text)
    audio_file = "response.mp3"
    tts.save(audio_file)
    return audio_file

# Function to autoplay audio in Streamlit
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "Hi! How can I assist you today?"}
    ]

# Streamlit App UI
st.title("Conversational Text-to-Speech Chatbot")

# Display conversation history
for message in st.session_state.messages[1:]:  # Skip the system message for display
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Assistant:** {message['content']}")

# User input
user_input = st.text_input("Type your question:")

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response from OpenAI GPT
    with st.spinner("Thinking..."):
        assistant_response = get_llm_response(st.session_state.messages)

    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Display assistant response
    st.markdown(f"**Assistant:** {assistant_response}")

    # Convert response to speech and autoplay
    with st.spinner("Generating audio..."):
        audio_file = text_to_speech(assistant_response)
        autoplay_audio(audio_file)

    


