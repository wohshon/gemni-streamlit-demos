import streamlit as st

from vertexai.generative_models import GenerativeModel, Part, Image



# Create a title and header for the app
st.title("Test drive Gemini Model")
st.header("Single turn, text and multimodal (images)")

option = st.selectbox(
   "Choose a model",
   ("gemini-1.5-flash-001","gemini-1.5-pro-001"),
   index=None,
   placeholder="Select model...",
)

mode = st.selectbox(
   "Text or multimodal? (only images for multimodal now)",
   ("text","multimodal"),
   index=None,
   placeholder="Select mode...",
)

if option:
   # Load Gemini Pro
   # gemini_pro_model = GenerativeModel("gemini-1.0-pro")
   # Load Gemini Pro
   gemini_pro_model = GenerativeModel(option)

   if mode == 'multimodal': 
      uploaded_file = st.file_uploader("Choose a file")
   
      if uploaded_file is not None:
         # To read file as bytes:
         bytes_data = uploaded_file.getvalue()
         # st.write(bytes_data)
         print(uploaded_file.name, uploaded_file.type)
         st.image(bytes_data)
         img = Part.from_data(bytes_data, mime_type=f"{uploaded_file.type}") 
         # img = Part.from_data(bytes_data) 
      # Create a text input field
      text = st.text_input("Enter some text")   
      # Create a button
      if st.button("Submit"):
         model_response = gemini_pro_model.generate_content([text,img ])
         print("model_response\n",model_response)
         # Display the text that was returned
         st.write(f" {model_response.candidates[0].content.parts[0].text}")
   else:
      text = st.text_input("Enter some text")   
      # Create a button
      if st.button("Submit"):
         model_response = gemini_pro_model.generate_content(text)
         print("model_response\n",model_response)
         # Display the text that was returned
         st.write(f" from {option}:")
         st.write(f" {model_response.candidates[0].content.parts[0].text}")