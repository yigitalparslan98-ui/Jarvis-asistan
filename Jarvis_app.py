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

    .fixed-bottom {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        max-width: 700px;
        display: flex;
        gap: 10px;
        z-index: 999;
        background: white;
        padding: 10px;
    }

    div[data-testid="stChatMessage"] { 
        background-color: #f5f5f7 !important; border-radius: 18px !important; 
        padding: 18px !important; margin-bottom: 12px !important; border: none !important;
    }
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
        // Streamlit'e veriyi gizli bir input üzerinden gönderiyoruz
        const input = window.parent.document.querySelectorAll('input[type="text"]')[0];
        input.value = transcript;
        input.dispatchEvent(new Event('input', {bubbles: true}));
    };
    </script>
    """
    st.components.v1.html(js, height=0)

client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages = []

def jarvis_brain(soru, oran):
    if not client: return "Sinyal hatası."
    alay = f"Alaycı ol (Seviye: {oran}/100)." if oran > 30 else "Profesyonel ol."
    try:
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": f"Sen JARVIS'sin. {alay} Kısa cevap ver. Efendim de."}, {"role": "user", "content": soru}],
            temperature=0.7,
        )
        return compl.choices[0].message.content
    except: return "Sistem meşgul."

alay_orani = st.slider("Alaycılık (%)", 0, 100, 20)
st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

# Mesajları listele (Alt panele yer açmak için padding eklendi)
st.container()
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])
st.write("") # Boşluk
st.write("") 

with st.container():
    c1, c2 = st.columns([0.85, 0.15])
    with c1:
        u_input = st.text_input("", key="main_input", placeholder="Bir komut verin...", label_visibility="collapsed")
    with c2:
        mic_clicked = st.button("🎙️")

if mic_clicked:
    listen_js()
    st.toast("Dinleniyor... Konuşun.")

if u_input:
    st.session_state.messages.append({"role": "user", "content": u_input})
    res = jarvis_brain(u_input, alay_orani)
    st.session_state.messages.append({"role": "assistant", "content": res})
    speak_js(res)
    st.rerun()






















