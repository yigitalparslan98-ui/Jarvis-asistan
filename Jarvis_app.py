import streamlit as st
import google.generativeai as genai
import time

# --- 1. GÖRSEL TASARIM ---
st.set_page_config(page_title="ALPARSLAN INDUSTRIES | JARVIS", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle, #001219 0%, #000000 100%);
        color: #00f2ff;
    }
    .stChatMessage {
        background: rgba(0, 242, 255, 0.07);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 20px;
    }
    h1 {
        font-family: 'Courier New', monospace;
        text-align: center;
        text-shadow: 0 0 25px #00f2ff;
    }
</style>
<h1>ALPARSLAN INDUSTRIES - JARVIS v3.1</h1>
""", unsafe_allow_html=True)

# --- 2. AKILLI MODEL BAĞLANTISI (404 SAVAR) ---
@st.cache_resource
def initialize_jarvis():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 404 Hatasını aşmak için sırayla tüm model isimlerini deniyoruz
        model_names = [
            'gemini-1.5-flash', 
            'gemini-1.5-flash-latest', 
            'gemini-pro', 
            'models/gemini-1.5-flash'
        ]
        
        for name in model_names:
            try:
                m = genai.GenerativeModel(name)
                # Modeli test et (boş cevap dönmezse çalışıyor demektir)
                m.generate_content("test")
                return m
            except:
                continue
        return None
    except Exception as e:
        return f"Kritik Hata: {e}"

model = initialize_jarvis()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Alparslan Industries sistemleri aktif. Emrinizdeyim efendim."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ETKİLEŞİM ---
if prompt := st.chat_input("Bir komut girin efendim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model is None or isinstance(model, str):
            st.error(f"Sistem hatası: API anahtarınız şu an hiçbir modeli çalıştırmıyor. {model}")
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
                st.error(f"Yanıt Hatası: {e}")












