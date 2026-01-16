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
        border-bottom: 2px solid rgba(0, 242, 255, 0.2);
    }
</style>
<h1>ALPARSLAN INDUSTRIES - JARVIS v3.1</h1>
""", unsafe_allow_html=True)

# --- 2. GÜVENLİ API VE MODEL BAĞLANTISI (404 HATASI ÇÖZÜMÜ) ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 404 HATASINI BİTİREN SATIR: 'models/' ön eki ile çağırıyoruz
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    else:
        st.error("Kritik Hata: API Anahtarı (Secrets) bulunamadı!")
        st.stop()
except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")
    st.stop()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Alparslan Industries sistemleri aktif. Hoş geldiniz efendim."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ETKİLEŞİM ---
if prompt := st.chat_input("Bir komut girin efendim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            # Yanıtı alırken güvenli metot kullanıyoruz
            response = model.generate_content(prompt)
            
            # Yazma efekti
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")











