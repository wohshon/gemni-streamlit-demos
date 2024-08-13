import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image, ChatSession


# vertexai.init(project=project_id, location=location)
def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

# Create a title and header for the app
st.title("Test drive Gemini Model - WIP")
st.header("Chat experience")

option = st.selectbox(
   "Choose a model",
   ("gemini-1.0-pro", "gemini-1.0-pro-vision"),
   index=None,
   placeholder="Select model...",
)

if option:
   # Load Gemini Pro
   # gemini_pro_model = GenerativeModel("gemini-1.0-pro")
   # Load Gemini Pro
   gemini_pro_model = GenerativeModel(option)
   text = st.text_input("Start charting")   
   if st.button("Submit"):
        chat = gemini_pro_model.start_chat()
        st.write(get_chat_response(chat, text))