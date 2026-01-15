import streamlit as st
import google.generativeai as genai

# --- GEMINI ZEKA AYARI ---
# Alttaki tırnak içine Google AI Studio'dan aldığın AIza... ile başlayan kodu yapıştır
genai.configure(api_key="AIzaSyBIL7Y0YaQ49tCYqu7aK3xIIKDj9GrZMNM")
model = genai.GenerativeModel('gemini-pro')

# --- SAYFA TASARIMI ---
st.set_page_config(page_title="JARVIS OS", layout="centered")

# Neon Başlık (Görsel şıklık için)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00d4ff; text-shadow: 0 0 15px #00d4ff; text-align: center; font-family: 'Courier New', monospace; }
    </style>
    <h1>JARVIS INTERFACE v2.0</h1>
    """, unsafe_allow_html=True)

# Hafıza sistemi (Konuşmanın devamlılığı için)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ VE CEVAP ---
prompt = st.chat_input("Bir emir verin efendim...")

if prompt:
    # Senin mesajın
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jarvis'in (Gemini) cevabı
    with st.chat_message("assistant"):
        try:
            # Google Gemini'den yanıt alınıyor
            response = model.generate_content(prompt)
            jarvis_response = response.text
            st.markdown(jarvis_response)
            st.session_state.messages.append({"role": "assistant", "content": jarvis_response})
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
            st.info("İpucu: API anahtarını tırnak içine doğru yapıştırdığından emin ol.")
