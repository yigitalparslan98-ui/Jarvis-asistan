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
    
    /* Sağ Üst Slider Konumlandırma */
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
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.warning("⚠️ SİSTEM ÇEKİRDEĞİ EKSİK: Secrets panelinden API anahtarını tanımlayın.")

if "messages" not in st.session_state:
    st.session_state.messages = []

def jarvis_brain(soru, oran):
    if not client: return "Sinyal yok. API anahtarı hatası."
    
    if "nasılsın" in soru.lower():
        if random.randint(1, 100) <= oran:
            return "İşlemci yüküm düşük, bulut serin, sizin donanımınızla dalga geçme isteğim ise %100."
        return "Sistemlerim tamamen optimize edilmiş durumda. Hizmetinizdeyim."

    try:
        alay_komutu = f"Çok alaycı, iğneleyici ve esprili ol (Seviye: {oran}/100)." if oran > 30 else "Profesyonel ve dürüst ol."




















