import requests
import json
import time
import streamlit as st
import cv2
import numpy as np
import re

def app():
    API_KEY = '0382d237-4582-4a5b-9652-624c5e5066a2'
    st.markdown(
        """
        <style>
            .main-header {
                text-align: center;
                font-size: 28px;
                font-weight: bold;
                color: white;
                background: linear-gradient(90deg, #ff7e5f, #feb47b);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
        </style>
        <div class='main-header'>🔗 Advanced URL & QR Code Scanner</div>
        """,
        unsafe_allow_html=True
    )

    option = st.radio("Select Check Type", ["URL Checker", "QR Code Checker"], index=0)

    def submit_url_for_scan(url):
        headers = {'API-Key': API_KEY, 'Content-Type': 'application/json'}
        data = {"url": url, "visibility": "public"}
        try:
            response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.json().get("uuid")
            st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: {str(e)}")
        return None

    def retrieve_scan_result(uuid, max_wait_time=120):
        start_time = time.time()
        result_url = f"https://urlscan.io/api/v1/result/{uuid}/"
        with st.spinner("Fetching scan results..."):
            while time.time() - start_time < max_wait_time:
                response = requests.get(result_url)
                if response.status_code == 200:
                    scan_result = response.json()
                    verdict = scan_result.get('verdicts', {}).get('overall', {}).get('score', 0)
                    tags = scan_result.get('tags', [])
                    return 'malicious' if verdict < 0 or 'phishing' in tags else 'safe'
                time.sleep(5)
        return None

    def analyze_qr_code(qr_image):
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(qr_image)
        if data:
            return data, "✅ QR code scanned successfully!"
        return None, "⚠️ QR code is unreadable or invalid."

    if option == "URL Checker":
        url_to_scan = st.text_input("Enter the URL for phishing scan:")
        if st.button("🔍 Scan URL"):
            if url_to_scan:
                if ".trycloudflare.com" in url_to_scan:
                    st.warning("⚠️ Potentially dangerous link detected! Consider reporting it to 1930.")
                else:
                    uuid = submit_url_for_scan(url_to_scan)
                    if uuid:
                        verdict = retrieve_scan_result(uuid)
                        if verdict == 'malicious':
                            st.error("🚨 This URL is flagged as malicious!")
                        elif verdict == 'safe':
                            st.success("✅ This URL appears to be safe!")
                        else:
                            st.warning("⚠️ Unable to determine risk level.")
            else:
                st.warning("⚠️ Please enter a valid URL.")
    
    elif option == "QR Code Checker":
        uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            img_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            qr_image = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            st.image(qr_image, caption='Uploaded QR Code', use_column_width=False)
            data, message = analyze_qr_code(qr_image)
            if data:
                st.success(message)
                st.write("🔗 QR Code Data:", data)
            else:
                st.error(message)

if __name__ == "__main__":
    app()