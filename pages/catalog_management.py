import streamlit as st
# import vertexai
from vertexai.generative_models import GenerativeModel, Part, Tool,GenerationConfig
# from vertexai.preview.generative_models import grounding
from google.cloud.sql.connector import Connector
import json
from util import get_suggeted_catagories

# Create a title and header for the app
st.title("Test drive Gemini")
st.header("Catalog Management and Enrichment")
st.write("This demo requires additional setup to connect to a vector database to get recommended categories")
st.write("It was tested with CLOUD SQL - MySQL as a vector db, refer to util.py if documentation is not completed yet")

st.markdown("""---""")
option = st.selectbox(
   "Choose a model",
   ("gemini-1.5-flash-001","gemini-1.5-pro-001"),
   index=0,
   placeholder="Select model...",
)

uploaded_file = st.file_uploader("Upload a product image")

# uploaded_txt = st.file_uploader("Upload a product description")

if uploaded_file is not None:
    print(f"file uploaded - {uploaded_file.type}")
    if uploaded_file.type.startswith("image"):
        print('ok')
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.image(bytes_data)
        img = Part.from_data(bytes_data, mime_type=f"{uploaded_file.type}") 
        context_text = st.text_area(label="Context / System Instruction",height=100,
            value="""You are an expert in understanding images of products for an ecommerce website and finding out their product categories and sub categories""")   
        prompt_text = st.text_area(label="prompt",height=500,
            value="""This is an image for a product on a ecommerce website, Please describe the product in the image and return in the following JSON format: 
{
    name:"<name of product>",
    brand:"<brand of product>",
    model:"<model of product>",
    colorway: "<colorway of product, if applicable>"
    description:"<description of product in less than 20 words, is it for Men or Women or Unisex>",
    primary_colors: [
        color_1,
        color_2,
        color_3
    ],
    gender: "<Men or Women or Unisex>"
    product_category: "<suggest a product category>",
    product_sub_category: "<suggest product sub category>",
}
If you are unable to get any of the required information, do not make it up.
""")

    else:
        print('nope')
        st.write("please uplooad image files only")
        
    if st.button("submit"):
        st.write("processing...")
        model = GenerativeModel(option)
        model_response = model.generate_content([prompt_text,img ])
        print("model_response\n",model_response)
        # Display the text that was returned
        text_output = model_response.candidates[0].content.parts[0].text
        st.write(f" {text_output}")
        #
        json_output = json.loads((text_output.replace("```json", "").replace("```", "")))
        print(json_output)
        st.write(json_output['product_category'])
        st.write(json_output['product_sub_category'])
        st.write(f"{json_output['product_category']} > {json_output['product_sub_category']}")
        # print(str(model_response.candidates[0].content.parts[0].text))
        test = []
        st.write('---------')
        test.append(f"{json_output['brand']} {json_output['name']} {json_output['model']} {json_output['description']} {json_output['gender']} {json_output['product_category']} > {json_output['product_sub_category']}")
        st.write("matching categories...")
        output = get_suggeted_catagories(test)
        print(output)
        st.write(f"Suggested categories by {option}:")
        st.write(output[0])
        st.write(output[1])
        # st.write(output[2])

