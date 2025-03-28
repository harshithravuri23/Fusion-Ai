import streamlit as st
import spacy
from heapq import nlargest
import time
import pyperclip
from textstat import flesch_reading_ease

# Load spaCy language model
@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

nlp = load_nlp_model()

# Summarizer function
def text_summarizer(text, summary_length):
    doc = nlp(text)
    word_frequencies = {}
    for word in doc:
        if not word.is_stop and not word.is_punct:
            word_frequencies[word.text.lower()] = word_frequencies.get(word.text.lower(), 0) + 1
    
    max_frequency = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency
    
    sentence_scores = {}
    for sentence in doc.sents:
        for word in sentence:
            if word.text.lower() in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word.text.lower()]
    
    summary_sentences = nlargest(summary_length, sentence_scores, key=sentence_scores.get)
    return " ".join([sentence.text for sentence in summary_sentences])

# Define the app function
def app():
    # Main Content - Header
    st.markdown("<div class='card'><h2>📚 Text Summarization 📚</h2></div>", unsafe_allow_html=True)

    # User Input
    input_text = st.text_area("Enter your text to summarize:", placeholder="Paste your article or paragraph...")

    # Display word and character count
    if input_text:
        st.write(f"**Word Count:** {len(input_text.split())} | **Character Count:** {len(input_text)}")
        st.write(f"**Readability Score:** {flesch_reading_ease(input_text):.2f}")

    # Summary Length Selector
    summary_length = st.slider("Select the number of sentences for the summary:", min_value=1, max_value=10, value=3)

    # Generate Summary Button
    if st.button("✨ Generate Summary ✨"):
        if input_text.strip():
            with st.spinner("Generating summary..."):
                time.sleep(1)
                summary = text_summarizer(input_text, summary_length)
                st.markdown("<div class='card'><h3>🔑 Summary 🔑</h3></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
                
                # Copy to Clipboard
                if st.button("📋 Copy to Clipboard"):
                    pyperclip.copy(summary)
                    st.success("Summary copied to clipboard!")
                    
                st.download_button(label="📥 Download Summary", data=summary, file_name="summary.txt", mime="text/plain")
        else:
            st.warning("Please enter some text to summarize.")
