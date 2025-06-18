# Aileen – Voice AI Bot

A voice-enabled AI chatbot that responds to questions with both text and speech output.

## Features

- Personal responses for specific questions about Aileen
- Fallback to GPT-4 for general questions
- Text-to-speech functionality
- Web interface built with Gradio

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Your OpenAI API Key**
   - Get your API key from: https://platform.openai.com/account/api-keys
   - Replace `"YOUR_OPENAI_API_KEY"` in `app.py` with your actual key:
   ```python
   openai.api_key = "sk-..."  # Your actual key
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

## Usage

Once the app is running, it will open a web interface in your browser. You can:

- Ask about Aileen's life story, superpower, growth areas, misconceptions, or what pushes her
- Ask any other question and get a GPT-4 response
- The bot will speak the response out loud and display it on screen

## Personal Responses

The bot has predefined responses for:
- "life story" - About Aileen's background and passion for AI
- "superpower" - About connecting ideas and taking action
- "grow" - About improving math, voice UX, and production systems
- "misconception" - About being perceived as quiet
- "push" - About learning by doing and building projects 