import streamlit as st
from google import genai
import pdfplumber
import time

st.set_page_config(page_title="Sampreeth AI Text Summarizer", page_icon="📝")
st.title("📝 Sampreeth AI Text Summarizer")
st.write("Paste text or upload a PDF to get a concise summary.")

# --- Input section ---
input_type = st.radio("Choose input type:", ["Paste text", "Upload PDF"])

text = ""
if input_type == "Paste text":
    text = st.text_area("Paste your article/text here", height=250)
else:
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        st.success(f"Extracted text from {len(pdf.pages)} pages.")

# --- Options ---
col1, col2 = st.columns(2)
with col1:
    summary_style = st.selectbox("Summary style", ["Concise paragraph", "Bullet points", "Executive summary"])
with col2:
    length = st.slider("Approx. summary length (words)", 50, 500, 150)

# --- Summarize button ---
if st.button("Summarize", type="primary"):
    if not text.strip():
        st.warning("Please paste some text or upload a PDF first.")
    else:
        with st.spinner("Summarizing..."):
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

            word_count = len(text.split())
            target_length = min(length, max(30, word_count // 2))

            prompt = f"""Summarize the following text in {summary_style.lower()} format.
The summary MUST be significantly shorter than the original text — no more than {target_length} words.
Do not pad, repeat, or elaborate beyond what's necessary. Keep only the key facts and main arguments.

Text:
{text}
"""
            summary = None
            last_error = None
            max_attempts = 3

            for attempt in range(1, max_attempts + 1):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                    summary = response.text
                    break  # success — stop retrying
                except Exception as e:
                    last_error = e
                    error_text = str(e)
                    # Only retry on temporary server-side overload, not on real errors
                    if "503" in error_text or "UNAVAILABLE" in error_text:
                        if attempt < max_attempts:
                            time.sleep(2 * attempt)  # wait a bit longer each retry
                            continue
                    break  # any other error, or out of retries — stop trying

            if summary:
                st.subheader("Summary")
                st.write(summary)
                st.caption(f"Original: ~{word_count} words → Summary: ~{len(summary.split())} words")
                st.download_button("Download summary as .txt", summary, file_name="summary.txt")
            else:
                if "503" in str(last_error) or "UNAVAILABLE" in str(last_error):
                    st.error("The AI model is temporarily busy handling a lot of requests. Please click Summarize again in a few seconds — this usually resolves quickly.")
                elif "429" in str(last_error) or "RESOURCE_EXHAUSTED" in str(last_error):
                    st.error("This app has hit its free daily usage limit. Please try again later, or come back tomorrow.")
                else:
                    st.error(f"Something went wrong: {last_error}")
