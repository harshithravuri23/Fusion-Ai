import streamlit as st
# Set page config
st.set_page_config(page_title="Fusion AI", page_icon="🤖", layout="wide")


from apps import image_generation
from apps import password_checker
from apps import text_summary
from apps import url_checker





# import spacy
# import os

# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     print("Downloading 'en_core_web_sm'...")
#     os.system("python -m spacy download en_core_web_sm")
#     nlp = spacy.load("en_core_web_sm")





# Apply custom styles for navbar
st.markdown(
    """
    <style>
        .nav-container {
            display: flex;
            justify-content: center;
            padding: 10px;
            background: linear-gradient(90deg, #ff8a00, #ff3e3e);
            border-radius: 10px;
        }
        .nav-button {
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: transparent;
            border: none;
            padding: 10px 20px;
            margin: 5px;
            cursor: pointer;
        }
        .nav-button:hover {
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Navigation Bar
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Home"):
        st.session_state.current_page = "Home"

with col2:
    if st.button("Image Generation"):
        st.session_state.current_page = "Image Generation"

with col3:
    if st.button("Password Checker"):
        st.session_state.current_page = "Password Checker"

with col4:
    if st.button("Text Summary"):
        st.session_state.current_page = "Text Summary"

with col5:
    if st.button("URL Checker"):
        st.session_state.current_page = "URL Checker"

st.markdown('</div>', unsafe_allow_html=True)

# Page Routing Logic
if st.session_state.current_page == "Home":
    st.title("🚀 Welcome to Fusion AI!")
    st.write("Select a tool from the navbar above.")

elif st.session_state.current_page == "Image Generation":
    image_generation.app()

elif st.session_state.current_page == "Password Checker":
    password_checker.app()

elif st.session_state.current_page == "Text Summary":
    text_summary.app()

elif st.session_state.current_page == "URL Checker":
    url_checker.app()














