import streamlit as st
import google.generativeai as genai
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="JARVIS OS", layout="centered")

# Görsel Stil
st.markdown("""
<style>
.stApp { background-color: #0d1a26; color: #00e6e6; }
h1 { text-align: center; color: #00e6e6; text-shadow: 0 0 15px #00e6e6; font-family: 'Courier New', monospace; }
</style>
<h1>JARVIS INTERFACE v2.1</h1>
""", unsafe_allow_html=True)

# --- GEMINI AYARI ---
# Kendi anahtarını buraya yapıştır:
genai.configure(api_key="AIzaSyBIL7Y0YaQ49tCYqu7aK3xIIKDj9GrZMNM")

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
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
            response = model.generate_content(prompt)
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Hata: {e}")
           



