import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import io
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("HUGGING_FACE_TOKEN")

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/ZB-Tech/Text-to-Image"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Streamlit Page
def app():
    st.subheader("🎨 AI Image Generator")
    prompt = st.text_input("Enter your text prompt:", placeholder="A futuristic city skyline at night with neon lights")

    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating your image..."):
                image = generate_image(prompt)

                if image:
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format="PNG")
                    img_bytes.seek(0)

                    st.image(img_bytes, caption="Generated Image", use_container_width=True)
                    st.download_button("Download Image", data=img_bytes, file_name="generated_image.png", mime="image/png")
                else:
                    st.error("Failed to generate image. Please try again.")
        else:
            st.warning("Please enter a prompt.")

# Function to call the API
def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        return None
