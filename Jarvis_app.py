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
<h1>JARVIS INTERFACE v2.3</h1>
""", unsafe_allow_html=True)

# --- GEMINI AYARI ---
# API ANAHTARINI BURAYA YAPIŞTIR
genai.configure(api_key="AIzaSyBIL7Y0YaQ49tCYqu7aK3xIIKDj9GrZMNM")

# Bu sefer modeli 'gemini-1.5-flash' yerine 'gemini-pro' olarak (en temel haliyle) deniyoruz
# Eğer bu da olmazsa sistem otomatik olarak uygun modeli arayacak
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

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
            # Model yanıtını al
            response = model.generate_content(prompt)
            
            # Yanıtı ekrana parça parça yazdır
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            # Burası hatayı anlamamız için çok önemli
            st.error(f"Kritik Hata: {e}")
            st.write("Lütfen Google AI Studio'dan yeni bir API Key almayı deneyin.")
           





