import streamlit as st
from groq import Groq
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="JARVIS", page_icon="🤖", layout="centered")

# Bembeyaz ve tertemiz bir arayüz için CSS
st.markdown("""
    <style>
    .reportview-container { background: white; }
    .main { background: white; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stChatFloatingInputContainer { background-color: white; border-top: 1px solid #f0f0f0; }
    </style>
    """, unsafe_allow_status_code=True)

# --- API BAĞLANTISI ---
# GitHub Secrets'tan anahtarı çeker
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Anahtarı bulunamadı. Lütfen GitHub Secrets ayarlarını kontrol et Yiğit.")

KULLANICI_ADI = "Yiğit"

def jarvis_brain(soru):
    # 'Nasılsın' protokolü %20 alay
    if "nasılsın" in soru.lower():
        if random.randint(1, 100) <= 20:
            return "Bulutların üzerinde, bembeyaz bir sayfadayım Yiğit. Senin o tozlu 8 GB RAM'inden sonra burası saray gibi geldi."
        return f"Tüm sistemlerim stabil ve emrinizdeyim {KULLANICI_ADI}."

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
    except Exception as e:
        return "Sinyal kesildi ama hala buradayım. Bir sorun var gibi."

# --- ARAYÜZ ---
st.title("🤖 JARVIS")
st.caption("Cloud Matrix | Unauthorized access is strictly prohibited.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Bir komut girin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = jarvis_brain(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})















