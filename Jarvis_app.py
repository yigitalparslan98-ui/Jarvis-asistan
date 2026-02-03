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
        position: fixed;
        top: 20px;
        right: 30px;
        width: 180px;
        z-index: 1000;
        background: rgba(255,255,255,0.9);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    div[data-testid="stChatMessage"] { 
        background-color: #f5f5f7 !important; 
        border-radius: 18px !important; 
        padding: 18px !important;
        margin-bottom: 12px !important;
        border: none !important;
    }
    .stMarkdown p { color: #1d1d1f; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .stChatFloatingInputContainer { background-color: rgba(255,255,255,0.8); backdrop-filter: blur(15px); }
    </style>
    """, unsafe_allow_html=True)

client = None
if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        client = None
else:
    st.warning("⚠️ API anahtarı Secrets panelinde bulunamadı.")

if "messages" not in st.session_state:
    st.session_state.messages = []

def jarvis_brain(soru, oran):
    if not client: return "Sinyal hatası: API anahtarı geçersiz."
    if "nasılsın" in soru.lower():
        if random.randint(1, 100) <= oran:
            return "İşlemci yüküm düşük, bulut serin, sizin donanımınızla dalga geçme isteğim ise %100."
        return "Sistemlerim tamamen optimize edilmiş durumda. Hizmetinizdeyim."
    try:
        alay = f"Çok alaycı ve iğneleyici ol (Seviye: {oran}/100)." if oran > 30 else "Profesyonel ol."
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen JARVIS'sin. Alparslan Industries asistanısın. {alay} Kısa cevap ver. Kullanıcıya 'Efendim' de."},
                {"role": "user", "content": soru}
            ],
            temperature=0.7,
        )
        return compl.choices[0].message.content
    except Exception as e:
        return f"Protokol Hatası: {str(e)}"

alay_orani = st.slider("Alaycılık (%)", 0, 100, 20)
st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Bir komut verin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner(" "):
            res = jarvis_brain(prompt, alay_orani)
            st.write(res)
    st.session_state.messages.append({"role": "assistant", "content": res})





















