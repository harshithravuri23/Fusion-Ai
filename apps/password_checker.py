import math
import streamlit as st
import string
import random
import re

def app():
    st.markdown("""
        <style>
        .gradient-header {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<p class='gradient-header'>🔐 Password Strength Checker</p>", unsafe_allow_html=True)
    
    class PasswordStrengthChecker:
        def check_strength(self, password):
            length = len(password)
            use_uppercase = bool(re.search(r'[A-Z]', password))
            use_lowercase = bool(re.search(r'[a-z]', password))
            use_numbers = bool(re.search(r'[0-9]', password))
            use_symbols = bool(re.search(r'[!@#$%^&*()_+{}\[\]:;\"\'<>,.?/\\|`~]', password))
            
            if length < 8:
                return "❌ Password should be at least 8 characters long.", None

            if not (use_uppercase or use_lowercase or use_numbers or use_symbols):
                return "❌ Password should include a mix of uppercase, lowercase, numbers, and symbols.", None

            entropy, time_seconds = self.calculate_cracking_time(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
            
            if time_seconds < 60:
                strength = "🔴 Very Weak (Cracked in seconds)"
            elif time_seconds < 3600:
                strength = "🟠 Weak (Cracked in minutes)"
            elif time_seconds < 86400:
                strength = "🟡 Moderate (Cracked in hours)"
            elif time_seconds < 31536000:
                strength = "🟢 Strong (Cracked in days)"
            else:
                strength = "🔵 Very Strong (Takes over a year to crack)"
            
            return strength, time_seconds

        def generate_password(self, length, use_uppercase, use_lowercase, use_numbers, use_symbols):
            characters = ""
            if use_uppercase:
                characters += string.ascii_uppercase
            if use_lowercase:
                characters += string.ascii_lowercase
            if use_numbers:
                characters += string.digits
            if use_symbols:
                characters += string.punctuation
            
            if not characters:
                return "❌ Please select at least one type of character."
            
            password = ''.join(random.choice(characters) for _ in range(length))
            return password

        def calculate_cracking_time(self, length, use_uppercase, use_lowercase, use_numbers, use_symbols, guesses_per_second=1e9):
            characters = 0
            if use_uppercase:
                characters += 26
            if use_lowercase:
                characters += 26
            if use_numbers:
                characters += 10
            if use_symbols:
                characters += 32
            
            if characters == 0:
                return "❌ Please select at least one type of character.", None
            
            entropy = length * math.log2(characters)
            total_combinations = 2 ** entropy
            time_seconds = total_combinations / guesses_per_second
            
            return entropy, time_seconds

        def run(self):
            password = st.text_input("Enter your password", type="password")
            
            if st.button("Check Strength"):
                if password:
                    strength_message, time_seconds = self.check_strength(password)
                    st.subheader(strength_message)
                    if time_seconds:
                        st.write(f"**Estimated Cracking Time:** {self.seconds_to_readable(time_seconds)}")
                else:
                    st.warning("Please enter a password.")
            
            st.markdown("---")
            st.subheader("🔑 Generate a Strong Password")
            
            length = st.slider("Password Length", min_value=8, max_value=24, value=12)
            use_uppercase = st.checkbox("Include Uppercase Letters", value=True)
            use_lowercase = st.checkbox("Include Lowercase Letters", value=True)
            use_numbers = st.checkbox("Include Numbers", value=True)
            use_symbols = st.checkbox("Include Symbols", value=True)
            
            if st.button("Generate Password"):
                generated_password = self.generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
                if "❌" not in generated_password:
                    st.success("Generated Password:")
                    st.code(generated_password)
                    entropy, time_seconds = self.calculate_cracking_time(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
                    st.write(f"**Estimated Cracking Time:** {self.seconds_to_readable(time_seconds)}")
                    st.write(f"**Entropy:** {entropy:.2f} bits")
                else:
                    st.error(generated_password)
        
        def seconds_to_readable(self, seconds):
            if seconds < 60:
                return f"{seconds:.2f} seconds"
            elif seconds < 3600:
                return f"{seconds / 60:.2f} minutes"
            elif seconds < 86400:
                return f"{seconds / 3600:.2f} hours"
            elif seconds < 31536000:
                return f"{seconds / 86400:.2f} days"
            else:
                return f"{seconds / 31536000:.2f} years"

    checker = PasswordStrengthChecker()
    checker.run()