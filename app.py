import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Groq Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Groq AI Assistant")
st.caption("Powered by Groq & openai/gpt-oss-120b")

# Initialize the Groq client using your custom variable 'x' from .env
api_key = os.getenv("x")

if not api_key:
    st.error("API key not found! Please make sure your .env file defines variable 'x'.")
    st.stop()

client = Groq(api_key=api_key)

# Initialize chat history in Streamlit session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, knowledgeable AI assistant."
        }
    ]

# Display prior chat messages (skip the system prompt in the UI display)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input via Streamlit's chat input box
if user_input := st.chat_input("Type your message here..."):
    # Append user message to history and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                chat_completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=st.session_state.messages
                )
                assistant_response = chat_completion.choices[0].message.content
                st.markdown(assistant_response)
                
                # Append assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            except Exception as e:
                st.error(f"An error occurred: {e}")