import os
import zipfile
import requests
import urllib.parse
import streamlit as st
from bs4 import BeautifulSoup
import tinycss2
import jsbeautifier

DOWNLOADS_FOLDER = 'downloads'
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

def get_html_css_js(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    html = str(soup)
    css, js = "", ""
    
    for tag in soup.find_all('link', {'rel': 'stylesheet'}):
        css_url = urllib.parse.urljoin(url, tag['href'])
        css += requests.get(css_url).text
    
    for tag in soup.find_all('script', {'src': True}):
        js_url = urllib.parse.urljoin(url, tag['src'])
        js += requests.get(js_url).text
    
    return html, beautify_css(css), beautify_js(js)

def beautify_css(css_code):
    try:
        parsed_rules = tinycss2.parse_stylesheet(css_code, skip_whitespace=True)
        beautified_css = []

        for rule in parsed_rules:
            if rule.type == 'qualified-rule':
                selector = tinycss2.serialize(rule.prelude).strip()
                declarations = tinycss2.parse_declaration_list(rule.content)
                
                beautified_css.append(f"{selector} {{")
                for declaration in declarations:
                    if declaration.type == 'declaration':
                        prop = declaration.name
                        value = tinycss2.serialize(declaration.value).strip()
                        beautified_css.append(f"    {prop}: {value};")
                beautified_css.append("}\n")
            elif rule.type == 'error':
                print(f"CSS Parsing error: {rule.message}")

        return "\n".join(beautified_css)
    except tinycss2.CSSParseError as e:
        print(f"CSS Parsing error: {e}")
        return css_code

def beautify_js(js_code):
    return jsbeautifier.beautify(js_code)

def create_zip(website_folder):
    zip_filename = os.path.join(DOWNLOADS_FOLDER, 'cloned_website.zip')
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(website_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), website_folder))
    return zip_filename

st.set_page_config(page_title="Website Cloner", layout="centered", page_icon="🌐")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #ff5733;
    }
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #6c757d;
    }
    .stButton>button {
        background: linear-gradient(to right, #ff512f, #dd2476);
        color: white;
        font-weight: bold;
        border-radius: 25px;
        padding: 10px 20px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #dd2476, #ff512f);
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3);
        transform: scale(1.05);
    }
    </style>
    <h1 class='main-title'>🌐 Website Cloner</h1>
    <p class='sub-title'>Clone and download websites effortlessly!</p>
    """,
    unsafe_allow_html=True,
)

url = st.text_input("Enter the website URL to clone:", placeholder="https://example.com")

if st.button("Clone Website 🌍"):
    if url.strip():
        with st.spinner("Cloning in progress..."):
            website_folder = 'cloned_website'
            os.makedirs(website_folder, exist_ok=True)
            
            html, css, js = get_html_css_js(url)
            with open(os.path.join(website_folder, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html)
            with open(os.path.join(website_folder, 'styles.css'), 'w', encoding='utf-8') as f:
                f.write(css)
            with open(os.path.join(website_folder, 'scripts.js'), 'w', encoding='utf-8') as f:
                f.write(js)
            
            zip_file = create_zip(website_folder)
            st.success("Website cloned successfully!")
            st.download_button(label="Download Cloned Website 📥", data=open(zip_file, "rb"), file_name="cloned_website.zip", mime="application/zip")
    else:
        st.warning("Please enter a valid URL.")

st.markdown("<div style='text-align: center; margin-top: 30px;'>Built with ❤️ using Streamlit</div>", unsafe_allow_html=True)
