# Aileen – Voice AI Bot

A voice-enabled AI chatbot that responds to questions with both text and speech output.

## Features

- Personal responses for specific questions about Aileen
- Fallback to GPT-4 for general questions
- Text-to-speech functionality (ElevenLabs)
- Web interface built with Streamlit
- No coding required for users

## Setup (Local)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Your API Keys**
   - Create a file at `.streamlit/secrets.toml` with:
     ```toml
     ELEVENLABS_API_KEY = "your-elevenlabs-key"
     VOICE_ID = "your-elevenlabs-voice-id"
     API_KEY = "your-openrouter-key"
     ```

3. **Run the Application**
   ```bash
   streamlit run app_streamlit.py
   ```

## One-Click Web Demo (Recommended)

- Deploy this repo to [Streamlit Community Cloud](https://share.streamlit.io/)
- Add your API keys in the app's "Secrets" section
- Share your public app link with anyone—no install or coding needed!

## Usage

- Type your question or upload an audio file (WAV/MP3)
- The bot will answer in Aileen's style, with both text and voice
- All responses use your ElevenLabs voice

## Personal Responses

The bot has predefined responses for:
- "life story" - About Aileen's background and passion for AI
- "superpower" - About connecting ideas and taking action
- "grow" - About improving math, voice UX, and production systems
- "push" - About learning by doing and building projects 
