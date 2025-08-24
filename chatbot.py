import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Loads .env file into environment variables

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

MODELS = {
    "Llama-3-8B": "llama3-8b-8192",
    "Llama-3-70B": "llama3-70b-8192",
    "Mixtral-8x7B": "mixtral-8x7b-32768",
    "Gemma-7B": "gemma-7b-it"
}

def get_ai_response(messages, model):
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
        stream=False
    )
    return resp.choices[0].message.content
def main():
    st.title("🤖 AI Chatbot")
    st.sidebar.header("Settings")
    model_name = st.sidebar.selectbox("Model", list(MODELS.keys()))
    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "assistant", "content": "Hello! How can I help?"}
        ]
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Your message..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages += st.session_state.history
        with st.chat_message("assistant"):
            response = get_ai_response(messages, MODELS[model_name])
            st.write(response)
            st.session_state.history.append({"role": "assistant", "content": response})
if __name__ == "__main__":
    main()
