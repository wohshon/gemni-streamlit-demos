import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Tool,GenerationConfig
import cv2
import numpy as np
import json

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image
import io

# Create a title and header for the app
st.title("Test drive Gemini")
st.header("Defect Detection")
st.markdown("""---""")
option = st.selectbox(
   "Choose a model",
   ("gemini-1.5-flash-001","gemini-1.5-pro-001"),
   index=1,
   placeholder="Select model...",
)
uploaded_file = st.file_uploader("Upload a product image")

if uploaded_file is not None:
    print(f"file uploaded - {uploaded_file.type}")
    if uploaded_file.type.startswith("image"):
        print('ok')
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.image(bytes_data)
        img = Part.from_data(bytes_data, mime_type=f"{uploaded_file.type}") 
        context_text = st.text_area(label="Context / System Instruction",height=100,
            value="""You are an expert in understanding images of products for an ecommerce website and detecting defects from the photos""")   
        prompt_text = st.text_area(label="prompt",height=300,
            value="""    This is an image of a second hand product. Detect the following defects from the image:
    - Discolouration
    - Dent
    - Crack
    - Scratches
    - Stain
    - Missing part
    
    Return your answer in JSON format:
    {"defect_label": "",
    "bounding_box": "ymin xmin ymax xmax"
    }
""")
    else:
        print('nope')
        st.write("please uplooad image files only")

    if st.button("submit"):
        st.write("processing....")
        # model = GenerativeModel("gemini-1.5-flash-001")
        model = GenerativeModel(option)
        model_response = model.generate_content([prompt_text,img ])
        # print("model_response\n",model_response)
        # Display the text that was returned
        response = model_response.candidates[0].content.parts[0].text
        st.write(f"{response}")     
        print(f"{response}")
        clean_response = response.replace("```json", "").replace("```", "").replace("[","").replace("]","").strip()
        clean_response = "[" + clean_response + "]"
        response_json = json.loads(clean_response)   
        print(response_json)    

        im = image = Image.open(io.BytesIO(bytes_data))
        # get width and height 
        img_width = im.width 
        img_height = im.height 

        # # display width and height 
        print("The height of the image is: ", img_height) 
        print("The width of the image is: ", img_width) 

        # Create figure and axes
        fig, axes = plt.subplots(figsize=(30, 10))  # Adjust figsize as needed

        # Display the images on the axes
        axes.imshow(im)
        axes.set_title(option)  # Optional title
        # axes[1].imshow(im)
        # axes[1].set_title("Gemini 1.5 Pro")
        for response in response_json:
            if response['bounding_box'] == "":
                continue
            if response['bounding_box'] == "null":
                continue
            else:
                label = response['defect_label']
                ymin, xmin, ymax, xmax = response['bounding_box'].split(" ")
                x_min = int(xmin)/1000*img_width
                x_max = int(xmax)/1000*img_width
                y_min = int(ymin)/1000*img_height
                y_max = int(ymax)/1000*img_height        
                width = x_max - x_min
                height = y_max - y_min
                rect = patches.Rectangle((x_min, y_min), width, height, linewidth=2, edgecolor='b', facecolor='none')
                axes.add_patch(rect)
                axes.text(x_min-10, y_min-30, label, color='b', fontsize=10, bbox=dict(facecolor='white', alpha=0.5)) 

        # plt.show(); 
        st.pyplot(fig)