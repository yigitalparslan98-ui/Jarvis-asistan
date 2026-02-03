import streamlit as st
from groq import Groq
import random

st.set_page_config(page_title="JARVIS | Alparslan Industries", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main-title { font-size: 45px; font-weight: 800; color: #1d1d1f; margin-bottom: 0px; }
    .sub-title { font-size: 15px; color: #86868b; letter-spacing: 2px; margin-bottom: 30px; }
    div[data-testid="stChatMessage"] { 
        background-color: #f5f5f7 !important; 
        border-radius: 15px !important; 
        padding: 15px !important;
        margin-bottom: 10px !important;
        border: none !important;
    }
    .stMarkdown p { color: #1d1d1f; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; }
    .stChatFloatingInputContainer { background-color: rgba(255,255,255,0.8); backdrop-filter: blur(10px); }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎛️ PROTOKOL AYARLARI")
    alay_orani = st.slider("Alaycılık Seviyesi", 0, 100, 20)
    st.divider()
    st.caption("Alparslan Industries © 2026")

client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.warning("⚠️ SİSTEM ÇEKİRDEĞİ EKSİK: Secrets panelinden API anahtarını tanımlayın.")

if "messages" not in st.session_state:
    st.session_state.messages = []

def jarvis_brain(soru, oran):
    if not client:
        return "Sinyal yok. API anahtarı olmadan işlem yapamam."
    
    if "nasılsın" in soru.lower():
        if random.randint(1, 100) <= oran:
            return "İşlemci yüküm düşük, bulut serin, sizin donanımınızla dalga geçme isteğim ise %100."
        return "Sistemlerim tamamen optimize edilmiş durumda. Hizmetinizdeyim."

    try:
        alay_komutu = f"Alaycı ve iğneleyici ol (Seviye: {oran}/100)." if oran > 30 else "Profesyonel ve dürüst ol."
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen JARVIS'sin. Alparslan Industries ürünü zeki bir asistansın. {alay_komutu} Kısa cevaplar ver. Kullanıcıya 'Efendim' diye hitap et."},
                {"role": "user", "content": soru}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Protokol Hatası: {str(e)}"

st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Bir komut verin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünülüyor..."):
            response = jarvis_brain(prompt, alay_orani)
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})



















