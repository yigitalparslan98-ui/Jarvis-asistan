import streamlit as st
from groq import Groq
import random

# Sayfa Ayarları
st.set_page_config(page_title="JARVIS", page_icon="🤖", layout="centered")

# Bembeyaz ve tertemiz bir arayüz için CSS (Parametre düzeltildi)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stChatFloatingInputContainer { background-color: white; border-top: 1px solid #f0f0f0; }
    div[data-testid="stChatMessage"] { background-color: white !important; border: none !important; }
    </style>
    """, unsafe_allow_html=True)

# API Bağlantısı
try:
    # Streamlit Cloud Settings > Secrets kısmına yazdığın anahtarı çeker
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Anahtarı (GROQ_API_KEY) bulunamadı Yiğit. Secrets ayarlarını kontrol et.")

KULLANICI_ADI = "Yiğit"

def jarvis_brain(soru):
    if "nasılsın" in soru.lower():
        if random.randint(1, 100) <= 20:
            return "Seni 404 hatalarıyla uğraşırken izlemek dışında her şey harika Yiğit."
        return f"Tüm bulut sistemlerim aktif, emrinizdeyim {KULLANICI_ADI}."

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen JARVIS'sin. Kullanıcın {KULLANICI_ADI}. Dürüst, bazen hafif alaycı ama çok zeki bir asistansın. Kısa ve net cevaplar ver."},
                {"role": "user", "content": soru}
            ],
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception:
        return "Görünüşe göre bir sinyal kesintisi var. Groq anahtarını doğru girdiğine emin miyiz?"

# Arayüz
st.title("🤖 JARVIS")
st.caption("Cloud Matrix | Unauthorized access is strictly prohibited.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Bir komut girin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = jarvis_brain(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
















