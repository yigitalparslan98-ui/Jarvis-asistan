import streamlit as st
import google.generativeai as genai
import time

# --- 1. SAYFA VE TASARIM AYARLARI ---
st.set_page_config(page_title="JARVIS OS v3.0", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle, #001219 0%, #000000 100%);
        color: #00f2ff;
    }
    .stChatMessage {
        background: rgba(0, 242, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
    }
    h1 {
        font-family: 'Courier New', monospace;
        text-align: center;
        text-shadow: 0 0 20px #00f2ff;
        letter-spacing: 5px;
    }
</style>
<h1>STARK INDUSTRIES - JARVIS v3.0</h1>
""", unsafe_allow_html=True)

# --- 2. GÜVENLİ API BAĞLANTISI ---
try:
    # Anahtar artık kodda değil, Streamlit Secrets panelinde durmalı
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Sistem Hatası: API Anahtarı (Secrets) yapılandırılmadı!")
    st.info("Lütfen Streamlit Cloud ayarlarından 'GOOGLE_API_KEY' ekleyin.")
    st.stop()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sistemler çevrimiçi. Size nasıl yardımcı olabilirim efendim?"}
    ]

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ETKİLEŞİM VE CEVAP ---
if prompt := st.chat_input("Bir komut girin efendim..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jarvis'in cevabı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Gemini'den yanıt al
            response = model.generate_content(prompt)
            jarvis_text = response.text
            
            # Yazma animasyonu (Realistik görünüm)
            for chunk in jarvis_text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")







