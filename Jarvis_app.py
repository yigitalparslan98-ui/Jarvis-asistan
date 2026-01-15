import streamlit as st
import google.generativeai as genai
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="JARVIS OS", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #0d1a26; color: #00e6e6; }
h1 { text-align: center; color: #00e6e6; text-shadow: 0 0 15px #00e6e6; font-family: 'Courier New', monospace; }
</style>
<h1>JARVIS INTERFACE v2.2</h1>
""", unsafe_allow_html=True)

# --- GEMINI AYARI ---
# API ANAHTARINI BURAYA YAPIŞTIR
genai.configure(api_key="AIzaSyB0RDQIvAUH_EychviIY8dgE1pj5M30Hm4")

# Hata Veren Satırın En Garantili Hali (v1beta yerine doğrudan models/gemini-1.5-flash-latest)
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Model yükleme hatası: {e}")

# --- HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ VE CEVAP ---
prompt = st.chat_input("Emredin efendim...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # Yanıt oluşturma
            response = model.generate_content(prompt)
            
            # Harf harf yazdırma efekti
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
            st.info("İpucu: Eğer hala 404 alıyorsanız, Google AI Studio'da API anahtarınızın yanındaki 'Model' listesinde hangi modellerin açık olduğunu kontrol edin.")
           




