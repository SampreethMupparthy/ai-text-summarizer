# 📝 Sampreeth AI Text Summarizer

A web app that generates concise summaries from pasted text or uploaded PDFs, powered by Google's Gemini API.

## Features
- Paste raw text or upload a PDF
- Choose summary style: paragraph, bullet points, or executive summary
- Adjustable summary length
- Download the summary as a .txt file
- Word count comparison (original vs summary)

## Tech Stack
- **Frontend/Backend:** Streamlit
- **AI Model:** Google Gemini API
- **PDF Parsing:** pdfplumber

## How it works
1. User provides input (text or PDF)
2. If a PDF, text is extracted using pdfplumber
3. A prompt is built based on the chosen style/length
4. Gemini API generates the summary
5. Result is shown with word-count stats and a download option

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

Add your Gemini API key in `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-key-here"
```

## Live Demo

([Try the live app](https://sampreeth-ai-text-summarizer.streamlit.app))

## What I learned
Building this helped me understand how to work with LLM APIs, structure prompts for consistent output length, handle PDF text extraction, and deploy a Python web app end-to-end.

## Author

**Sampreeth Mupparthy**
[GitHub](https://github.com/SampreethMupparthy) · [LinkedIn](https://linkedin.com/in/sampreeth-mupparthy) [Try the live app](https://sampreeth-ai-text-summarizer.streamlit.app)
