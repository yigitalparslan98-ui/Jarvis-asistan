import streamlit as st
from groq import Groq
import random

st.set_page_config(page_title="JARVIS | Alparslan Industries", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main-title { font-size: 65px; font-weight: 900; color: #1d1d1f; margin-bottom: 0px; letter-spacing: -2px; }
    .sub-title { font-size: 16px; color: #86868b; letter-spacing: 3px; margin-bottom: 40px; font-weight: 500; }
    .stSlider {
        position: fixed; top: 20px; right: 30px; width: 180px; z-index: 1000;
        background: rgba(255,255,255,0.9); padding: 10px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div[data-testid="stChatMessage"] { 
        background-color: #f5f5f7 !important; border-radius: 18px !important; 
        padding: 18px !important; margin-bottom: 12px !important; border: none !important;
    }
    /* Mikrofon ve Giriş Alanı Yan Yana */
    .input-container { display: flex; align-items: center; gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

def speak_js(text):
    if text:
        clean_text = text.replace("'", "").replace("\n", " ")
        js = f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'tr-TR'; window.speechSynthesis.speak(msg);</script>"
        st.components.v1.html(js, height=0)

def listen_js():
    js = """
    <script>
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'tr-TR';
    recognition.start();
    recognition.onresult = function(event) {
        var transcript = event.results[0][0].transcript;
        window.parent.postMessage({type: 'mic_result', text: transcript}, '*');
    };
    </script>
    """
    st.components.v1.html(js, height=0)

client = None
if "GROQ_API_KEY" in st.secrets:
    try: client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: client = None

if "messages" not in st.session_state: st.session_state.messages = []

def jarvis_brain(soru, oran):
    if not client: return "Sinyal hatası."
    try:
        alay = f"Alaycı ol (Seviye: {oran}/100)." if oran > 30 else "Profesyonel ol."
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen JARVIS'sin. Alparslan Industries asistanısın. {alay} Kısa cevap ver. Efendim de."},
                {"role": "user", "content": soru}
            ],
            temperature=0.7,
        )
        return compl.choices[0].message.content
    except: return "Bağlantı hatası."

alay_orani = st.slider("Alaycılık (%)", 0, 100, 20)
st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# Giriş Bölümü (Yan Yana)
col1, col2 = st.columns([0.9, 0.1])
with col1:
    user_input = st.text_input("", placeholder="Komutunuzu buraya yazın veya mikrofonu kullanın...", key="widget_input", label_visibility="collapsed")
with col2:
    if st.button("🎙️"):
        listen_js()

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        res = jarvis_brain(user_input, alay_orani)
        st.write(res)
        speak_js(res)
    st.session_state.messages.append({"role": "assistant", "content": res})
    st.rerun()





















