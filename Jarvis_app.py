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
    .stChatFloatingInputContainer { background-color: rgba(255,255,255,0.8); backdrop-filter: blur(15px); }
    </style>
    """, unsafe_allow_html=True)

def speak_js(text):
    if text:
        clean_text = text.replace("'", "").replace("\n", " ")
        js_code = f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'tr-TR';
        window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js_code, height=0)

def listen_js():
    js_code = """
    <script>
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'tr-TR';
    recognition.start();
    recognition.onresult = function(event) {
        var transcript = event.results[0][0].transcript;
        const streamlitDoc = window.parent.document;
        const chatInput = streamlitDoc.querySelector('textarea[aria-label="Bir komut verin..."]');
        if (chatInput) {
            chatInput.value = transcript;
            chatInput.dispatchEvent(new Event('input', { bubbles: true }));
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
            nativeInputValueSetter.call(chatInput, transcript);
            chatInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    };
    </script>
    """
    st.components.v1.html(js_code, height=0)

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

if prompt := st.chat_input("Bir komut verin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        res = jarvis_brain(prompt, alay_orani)
        st.write(res)
        speak_js(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

st.divider()
if st.button("🎙️ Sesli Komut Ver"):
    listen_js()
    st.info("Dinleniyor... Konuşun ve metin kutusuna dolmasını bekleyin.")





















