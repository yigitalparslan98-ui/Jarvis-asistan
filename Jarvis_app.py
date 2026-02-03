import streamlit as st
from groq import Groq
import random

st.set_page_config(page_title="JARVIS | Alparslan Industries", page_icon="🤖", layout="centered")

# --- CSS İLE GÖRSEL TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* DEVASA BAŞLIK */
    .main-title { 
        font-size: 120px; /* İsteğin üzerine devasa yapıldı */
        font-weight: 900; 
        color: #1d1d1f; 
        text-align: center; 
        margin-top: 20px; 
        line-height: 1.1;
        letter-spacing: -5px; 
    }
    
    .sub-title { 
        font-size: 24px; 
        color: #86868b; 
        text-align: center; 
        letter-spacing: 8px; 
        margin-bottom: 80px; 
        font-weight: 600; 
        text-transform: uppercase;
    }
    
    /* Mesaj Baloncukları */
    div[data-testid="stChatMessage"] { 
        background-color: #f5f5f7 !important; border-radius: 18px !important; 
        padding: 18px !important; margin-bottom: 12px !important; border: none !important;
    }

    /* EN ALTA SABİTLENMİŞ PANEL (THE DOCK) */
    .fixed-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 20px 15%; /* Kenarlardan boşluk */
        border-top: 1px solid #e5e5e5;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
    }
    
    /* Sayfa içeriğinin panelin altında kalmaması için boşluk */
    .block-container { padding-bottom: 180px; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM ---
client = None
if "GROQ_API_KEY" in st.secrets:
    try: client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: client = None

if "messages" not in st.session_state: st.session_state.messages = []

# --- JS KONUŞMA ---
def speak_js(text):
    if text:
        clean = text.replace("'", "").replace("\n", " ")
        st.components.v1.html(f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean}'); msg.lang = 'tr-TR'; window.speechSynthesis.speak(msg);</script>", height=0)

# --- BEYİN ---
def jarvis_brain(soru, oran):
    if not client: return "Sinyal yok."
    alay = f"Alaycı ol (Seviye: {oran}/100)." if oran > 30 else "Profesyonel ol."
    try:
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": f"Sen JARVIS'sin. {alay} Çok kısa cevap ver."}, {"role": "user", "content": soru}],
            temperature=0.7,
        )
        return compl.choices[0].message.content
    except: return "Bağlantı hatası."

# --- SAĞ ÜST SLIDER ---
st.markdown("""<style>div[data-testid="stSlider"] { position: fixed; top: 20px; right: 20px; width: 200px; z-index: 10000; background: white; padding: 10px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }</style>""", unsafe_allow_html=True)
alay_orani = st.slider("Alaycılık Modu", 0, 100, 20)

# --- GÖRÜNÜM ---
st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

# Mesajları Göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# --- SABİT ALT PANEL (INPUT & MIC) ---
with st.container():
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.85, 0.15])
    with c1:
        # Enter'a basınca çalışması için form
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("", placeholder="Komut verin...", label_visibility="collapsed")
            submit = st.form_submit_button("GÖNDER", use_container_width=True)
    with c2:
        # Mikrofon butonu
        mic = st.button("🎙️")
    st.markdown('</div>', unsafe_allow_html=True)

# --- MANTIK ---
if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    res = jarvis_brain(user_input, alay_orani)
    st.session_state.messages.append({"role": "assistant", "content": res})
    speak_js(res)
    st.rerun()

if mic:
    # Mikrofon JS Kodu
    js = """
    <script>
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'tr-TR';
    recognition.start();
    recognition.onresult = function(e) {
        var txt = e.results[0][0].transcript;
        var inputs = window.parent.document.querySelectorAll('input[type="text"]');
        if(inputs.length > 0) {
            inputs[0].value = txt;
            inputs[0].dispatchEvent(new Event('input', {bubbles: true}));
            inputs[0].dispatchEvent(new Event('change', {bubbles: true}));
        }
    }
    </script>
    """
    st.components.v1.html(js, height=0)
    st.toast("Dinleniyor...")
























