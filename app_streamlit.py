import streamlit as st
import requests
import speech_recognition as sr
import io
import streamlit.components.v1 as components
import base64
from elevenlabs import generate, Voice, set_api_key

# --- ElevenLabs API credentials ---
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
VOICE_ID = st.secrets["VOICE_ID"]
API_KEY = st.secrets["API_KEY"]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Poppins:wght@400;700&display=swap');
    html, body, .stApp {
        background: linear-gradient(120deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #f3f6fa;
        font-family: 'Inter', 'Poppins', sans-serif;
    }
    .main-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff006e, #8338ec, #06ffa5);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-move 3s ease-in-out infinite;
        letter-spacing: 2px;
        margin-bottom: 0.2em;
        text-align: center;
    }
    @keyframes gradient-move {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .subtitle {
        font-size: 1.3rem;
        color: #b0b8c9;
        text-align: center;
        margin-bottom: 2em;
    }
    .glass-card {
        background: rgba(26,26,34,0.7);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 2.5px solid;
        border-image: linear-gradient(90deg, #ff006e, #8338ec, #06ffa5) 1;
        padding: 2.5em 2em 2em 2em;
        margin-bottom: 2em;
        margin-left: auto;
        margin-right: auto;
        max-width: 420px;
        width: 100%;
        transition: box-shadow 0.3s;
    }
    @media (max-width: 600px) {
        .glass-card {
            padding: 1.2em 0.7em 1em 0.7em;
            max-width: 98vw;
        }
    }
    .glass-card:hover {
        box-shadow: 0 12px 48px 0 #ff006e44, 0 2px 8px #06ffa544;
        border-image: linear-gradient(90deg, #fb8500, #ff006e) 1;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ff006e;
        margin-bottom: 1em;
        letter-spacing: 1px;
    }
    .input-label {
        color: #06ffa5;
        font-weight: 600;
        margin-bottom: 0.5em;
        font-size: 1.1rem;
    }
    .stTextArea textarea, .stTextInput>div>div>input {
        background: rgba(20,20,30,0.8);
        color: #fff;
        border-radius: 12px;
        border: 1.5px solid #8338ec;
        font-size: 1.1rem;
        padding: 1em;
        box-shadow: 0 2px 8px #8338ec22;
        transition: border 0.2s, box-shadow 0.2s;
    }
    .stTextArea textarea:focus, .stTextInput>div>div>input:focus {
        border: 1.5px solid #ff006e;
        box-shadow: 0 0 0 2px #ff006e44;
    }
    .stFileUploader, .stAudio {
        background: rgba(20,20,30,0.8);
        border-radius: 12px;
        padding: 1em;
        border: 1.5px solid #00d4ff;
        box-shadow: 0 2px 8px #00d4ff22;
    }
    .stFileUploader:hover, .stAudio:hover {
        border: 1.5px solid #ff006e;
        box-shadow: 0 0 0 2px #ff006e44;
    }
    .gradient-btn button {
        background: linear-gradient(90deg, #ff006e, #8338ec);
        color: #fff;
        border: none;
        border-radius: 16px;
        font-size: 1.2rem;
        font-weight: 700;
        padding: 0.8em 2.2em;
        box-shadow: 0 4px 24px #ff006e44;
        transition: transform 0.15s, box-shadow 0.15s, background 0.3s;
        outline: none;
        margin-top: 1em;
        margin-bottom: 1em;
        animation: pulse 2s infinite;
    }
    .gradient-btn button:hover {
        background: linear-gradient(90deg, #fb8500, #ff006e);
        transform: scale(1.04);
        box-shadow: 0 8px 32px #fb850088, 0 2px 8px #06ffa544;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 #ff006e44; }
        70% { box-shadow: 0 0 0 12px #ff006e11; }
        100% { box-shadow: 0 0 0 0 #ff006e44; }
    }
    .response-bubble {
        background: rgba(30, 30, 40, 0.85);
        border-radius: 24px 24px 8px 24px;
        padding: 2em 2em 1.5em 2em;
        margin-top: 1em;
        font-size: 1.25rem;
        color: #fff;
        box-shadow: 0 8px 32px #8338ec33, 0 2px 8px #06ffa544;
        border: 2.5px solid;
        border-image: linear-gradient(90deg, #ff006e, #8338ec, #06ffa5) 1;
        position: relative;
        min-height: 60px;
        transition: box-shadow 0.3s, border 0.3s;
    }
    .response-bubble:before {
        content: '';
        position: absolute;
        left: 24px;
        bottom: -16px;
        width: 32px;
        height: 32px;
        background: rgba(30, 30, 40, 0.85);
        border-radius: 0 0 16px 16px;
        box-shadow: 0 8px 32px #8338ec33;
        border-bottom: 2.5px solid #8338ec;
        z-index: 1;
    }
    .avatar {
        width: 64px; height: 64px;
        border-radius: 50%;
        border: 3px solid #ff006e;
        box-shadow: 0 0 24px #ff006e88, 0 2px 8px #06ffa544;
        margin-right: 18px;
        float: left;
        animation: avatar-pulse 2s infinite;
    }
    @keyframes avatar-pulse {
        0% { box-shadow: 0 0 0 0 #ff006e44; }
        70% { box-shadow: 0 0 0 16px #ff006e11; }
        100% { box-shadow: 0 0 0 0 #ff006e44; }
    }
    .waveform {
        width: 100%;
        height: 48px;
        margin-top: 1em;
        margin-bottom: 1em;
        display: block;
    }
    .stSidebar {
        background: rgba(20,20,30,0.85) !important;
        border-right: 2px solid #8338ec;
        box-shadow: 8px 0 32px #8338ec22;
    }
    .stSpinner > div > div {
        border-top-color: #ff006e !important;
        border-right-color: #8338ec !important;
    }
    /* Animated background orbs */
    .orbs-bg {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    }
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(32px);
        opacity: 0.25;
        animation: float 12s infinite alternate ease-in-out;
    }
    .orb1 { width: 320px; height: 320px; background: #ff006e; left: 10vw; top: 10vh; animation-delay: 0s; }
    .orb2 { width: 220px; height: 220px; background: #8338ec; left: 60vw; top: 30vh; animation-delay: 2s; }
    .orb3 { width: 180px; height: 180px; background: #06ffa5; left: 40vw; top: 70vh; animation-delay: 4s; }
    @keyframes float {
        0% { transform: translateY(0) scale(1); }
        100% { transform: translateY(-40px) scale(1.08); }
    }
    /* Focus indicators */
    textarea:focus, input:focus, button:focus {
        outline: 2.5px solid #fb8500 !important;
        outline-offset: 2px;
    }
    .custom-audio-player .stAudio > audio {
        width: 100% !important;
        min-width: 350px;
        max-width: 700px;
        height: 48px;
        border-radius: 16px;
        background: rgba(26,26,34,0.7);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 2.5px solid #8338ec;
        margin-top: 0.5em;
        margin-bottom: 1.5em;
        outline: none;
    }
    .custom-audio-player {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .audio-glass-card {
        background: rgba(26,26,34,0.7);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 2.5px solid;
        border-image: linear-gradient(90deg, #ff006e, #8338ec, #06ffa5) 1;
        padding: 2.5em 2em 2.5em 2em;
        margin: 2em auto 2em auto;
        max-width: 700px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .audio-glass-card .stAudio > audio {
        width: 100% !important;
        min-width: 350px;
        max-width: 650px;
        min-height: 80px;
        height: 80px;
        background: transparent;
        margin: 1em 0 1em 0;
        outline: none;
        border: none;
        box-shadow: none;
    }
    </style>
    <div class='orbs-bg'>
        <div class='orb orb1'></div>
        <div class='orb orb2'></div>
        <div class='orb orb3'></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Aileen – Voice AI Bot", page_icon="🤖", layout="centered")
st.markdown("<div class='main-title'>🤖 Aileen – Voice AI Bot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask me anything! I'll answer with text and voice.<br>Type your question, or upload audio, then press Submit.</div>", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("<div class='section-title'>About</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div class='sidebar-content'>
    <b>Aileen – Voice AI Bot</b><br><br>
    <ul style='padding-left:18px;'>
      <li>Text and voice input (via file upload)</li>
      <li>Powered by OpenRouter & ElevenLabs</li>
    </ul>
    <i style='color:#ff006e;'>Tip: Upload an audio file for voice input!</i>
    </div>
    """,
    unsafe_allow_html=True
)

# --- ElevenLabs TTS ---
def elevenlabs_tts(text):
    try:
        set_api_key(ELEVENLABS_API_KEY)
        audio = generate(
            text=text,
            voice=Voice(voice_id=VOICE_ID),
            model="eleven_monolingual_v1"
        )
        return audio  # this is already in byte format
    except Exception as e:
        st.error(f"ElevenLabs error: {e}")
        return None

# --- Speech-to-text ---
def transcribe_audio(audio_bytes):
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        return f"[Voice recognition error: {e}]"

# --- Personal responses ---
def get_answer(prompt):
    lower = prompt.lower()
    if "life story" in lower:
        return "I'm Aileen, a recent grad passionate about AI. I've built agentic systems and love solving problems by building cool stuff."
    elif "superpower" in lower:
        return "Connecting ideas fast and taking action. I don't get stuck in planning – I build."
    elif "grow" in lower:
        return "Improving math for ML, voice UX, and building production systems."
    elif "misconception" in lower:
        return "That I'm too quiet — I just observe and then contribute deeply."
    elif "push" in lower:
        return "I throw myself into things I don't know and learn by doing. That's how I built my last few projects."
    else:
        try:
            system_prompt = (
                "You are Aileen, a recent grad passionate about AI. "
                "Answer all questions as if you are Aileen, using her style, background, and personality. "
                "Be authentic, personal, and specific."
            )
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            result = response.json()
            st.write(result)  # For debugging: show full API response
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"]
            else:
                st.error(f"API Error: {result}")
                return f"API Error: {result}"
        except Exception as e:
            st.error(f"API Error: {e}")
            return f"Error: {e}"

# --- Main UI ---
st.divider()

# --- Question Card ---
st.markdown("<div class='section-title'>Your Question</div>", unsafe_allow_html=True)
user_input = st.text_area("", placeholder="Type your question here...", height=80, key="text_input")

# --- Audio Upload Card ---
st.markdown("<div style='margin-top:10px; font-size:16px;'>Or upload an audio file:</div>", unsafe_allow_html=True)
audio_file = st.file_uploader("Upload audio (WAV/MP3)", type=["wav", "mp3"], key="audio_upload")
if audio_file is not None:
    audio_bytes = audio_file.read()
    try:
        transcribed_text = transcribe_audio(audio_bytes)
        st.success(f"Transcribed: {transcribed_text}")
        if not user_input:
            user_input = transcribed_text
    except Exception as e:
        st.warning(f"Voice recognition error: {e}")

# --- Response Card ---
st.markdown("<div class='section-title'>Aileen's Response</div>", unsafe_allow_html=True)
response_placeholder = st.empty()

submit = st.button("Submit", use_container_width=True, key="submit_btn", help="Send your question to Aileen")

if submit and user_input.strip():
    with st.spinner("Thinking..."):
        answer = get_answer(user_input)
    response_placeholder.markdown(f"<div class='glass-card response-bubble'>{answer}</div>", unsafe_allow_html=True)
    audio_bytes = elevenlabs_tts(answer)
    st.session_state['audio_bytes'] = audio_bytes if audio_bytes else None

# Audio player always visible after submit
if 'audio_bytes' in st.session_state and st.session_state['audio_bytes']:
    audio_bytes = st.session_state['audio_bytes']
    audio_b64 = base64.b64encode(audio_bytes).decode()
    audio_src = f"data:audio/mp3;base64,{audio_b64}"
    wavesurfer_html = f'''
    <div class="audio-glass-card">
      <div id="waveform"></div>
      <div style="display:flex;justify-content:center;margin-top:1em;">
        <button id="playPause" style="background:linear-gradient(90deg,#ff006e,#8338ec);color:#fff;border:none;border-radius:16px;font-size:1.2rem;font-weight:700;padding:0.5em 2em;box-shadow:0 4px 24px #ff006e44;cursor:pointer;">Play/Pause</button>
      </div>
    </div>
    <script src="https://unpkg.com/wavesurfer.js"></script>
    <script>
      var wavesurfer = WaveSurfer.create({{
        container: '#waveform',
        waveColor: '#8338ec',
        progressColor: '#ff006e',
        backgroundColor: 'rgba(26,26,34,0.7)',
        barWidth: 3,
        barRadius: 3,
        height: 80,
        responsive: true,
        cursorColor: '#06ffa5',
      }});
      wavesurfer.load('{audio_src}');
      document.getElementById('playPause').onclick = function() {{
        wavesurfer.playPause();
      }};
    </script>
    '''
    components.html(wavesurfer_html, height=200) 