
            import streamlit as st
import google.generativeai as genai
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="JARVIS OS", layout="centered")

# Görsel Stil (Neon Tema)
st.markdown("""
    <style>
    .stApp { background-color: #0d1a26; color: #00e6e6; }
    h1 { text-align: center; color: #00e6e6; text-shadow: 0 0 15px #00e6e6; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: #1a2a3a; border-radius: 10px; border-left: 3px solid #00e6e6; }
    </style>
    <h1>JARVIS INTERFACE v2.1</h1>
    """, unsafe_allow_html=True)

# --- GEMINI HATA GİDERME AYARI ---
# API anahtarını buraya yapıştır
genai.configure(api_key="AIzaSyBIL7Y0YaQ49tCYqu7aK3xIIKDj9GrZMNM")

# Hata Veren Satırı Bu Şekilde Güncelledik (En Sağlam Yol):
try:
    # Model ismini 'models/gemini-1.5-flash' şeklinde tam yol olarak belirttik
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Model yükleme hatası: {e}")

# --- HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ VE CEVAP ---
if prompt := st.chat_input("Emredin efendim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Cevap üretme
            response = model.generate_content(prompt)
            
            # Yazma animasyonu
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
            st.info("Eğer bu hatayı almaya devam ediyorsanız, API anahtarınızın 'Google AI Studio' üzerinden alındığından emin olun.")


