import streamlit as st
import google.generativeai as genai
import time

# --- SAYFA AYARLARI (Geniş Ekran) ---
st.set_page_config(page_title="JARVIS OS | Terminal", layout="wide")

# --- GERÇEKÇİ JARVIS TEMASI (CSS) ---
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
    /* Scrollbarı özelleştir */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #00f2ff; border-radius: 10px; }
</style>
<h1>STARK INDUSTRIES - JARVIS v3.0</h1>
""", unsafe_allow_html=True)

# --- API VE MODEL AYARI ---
# API ANAHTARINI AŞAĞIYA YAPIŞTIR
genai.configure(api_key="AIzaSyBhCEI1LEMr54a_dO1OqjeW77UoFnPt5iA")

# 404 Hatalarını Önleyen Akıllı Model Seçici
@st.cache_resource
def load_model():
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(m_name)
            # Modeli test et
            model.generate_content("test")
            return model
        except:
            continue
    return None

model = load_model()

# --- SOHBET SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler çevrimiçi. Size nasıl yardımcı olabilirim efendim?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bir komut girin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model is None:
            st.error("Üzgünüm efendim, tüm model bağlantıları başarısız oldu. Lütfen API anahtarınızı kontrol edin.")
        else:
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = model.generate_content(prompt)
                for chunk in response.text.split():
                    full_response += chunk + " "
                    time.sleep(0.04)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Bağlantı Kesildi: {e}")
           






