import streamlit as st
import os
import random
from dotenv import load_dotenv
import base64
from openai import OpenAI
from PIL import Image, ImageFilter

# Load environment variables
load_dotenv()
key = os.getenv('OPEN_AI_KEY')
MODEL = 'gpt-4o'
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Specify the folder containing images
IMAGE_FOLDER = "glics"  # Replace with your folder path

st.title('Listening to training images')
st.text("Images and response text may take time to load, images are blurred here for privacy")
st.text("Inspired by Tina Campt's book, Listening to Images, 2017")
st.text("Sometimes the algorithm refuses to analyse images of people, ironic given the purpose of such a data set - to train facial recognition")
st.button("listen to another image")
# Select a random image from the folder
if os.path.exists(IMAGE_FOLDER):
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if image_files:
        random_image = random.choice(image_files)
        random_image_path = os.path.join(IMAGE_FOLDER, random_image)

        # Open the image and apply a strong blur
        with Image.open(random_image_path) as img:
            blurred_image = img.filter(ImageFilter.GaussianBlur(15))  # Apply strong blur
            notblurred_image = img.filter(ImageFilter.GaussianBlur(1))  # Apply strong blur
            blurred_image.save("blurred_image.png")  # Save the blurred image for display
            notblurred_image.save("notblurred_image.png")
            #st.image(blurred_image, caption='Blurred Randomly Selected Image')
            st.image(blurred_image,"", 200)
        # Encode the blurred image
        #base64_image = encode_image("blurred_image.png")
        base64_image = encode_image("notblurred_image.png")
        # Make the API call
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Could you describe the image and create a narrative to highlight important details and provide recommendations. Provide Observations, important details, evidence for resistance, and ideas for further analysis with bullet points."},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ],
            temperature=0.0,
        )

        st.markdown(response.choices[0].message.content)
    else:
        st.error("No images found in the specified folder.")
else:
    st.error("The specified folder does not exist.")
