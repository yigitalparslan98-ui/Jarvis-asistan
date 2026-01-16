import streamlit as st
import google.generativeai as genai
import time

# --- 1. GÖRSEL TASARIM (REALİSTİK JARVIS TEMASI) ---
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
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
    }
    h1 {
        font-family: 'Courier New', monospace;
        text-align: center;
        text-shadow: 0 0 20px #00f2ff;
        letter-spacing: 5px;
        border-bottom: 1px solid rgba(0, 242, 255, 0.3);
        padding-bottom: 10px;
    }
    .stChatInputContainer {
        border-top: 1px solid rgba(0, 242, 255, 0.2);
    }
</style>
<h1>STARK INDUSTRIES - JARVIS v3.0</h1>
""", unsafe_allow_html=True)

# --- 2. GÜVENLİ API VE MODEL BAĞLANTISI ---
try:
    # Anahtarı Streamlit Secrets'tan alıyoruz
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 404 HATASINI ÖNLEYEN AKILLI SEÇİCİ
    @st.cache_resource
    def get_working_model():
        # Google'ın kabul edebileceği tüm varyasyonları sırayla dener
        test_names = [
            'gemini-1.5-flash', 
            'models/gemini-1.5-flash', 
            'gemini-pro', 
            'models/gemini-pro'
        ]
        for name in test_names:
            try:
                m = genai.GenerativeModel(name)
                # Küçük bir test sorgusu
                m.generate_content("test") 
                return m
            except:
                continue
        return None

    model = get_working_model()

except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")
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

# --- 4. ETKİLEŞİM VE YANIT SİSTEMİ ---
if prompt := st.chat_input("Bir komut girin efendim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model is None:
            st.error("Bağlantı Hatası: Uygun bir yapay zeka modeli bulunamadı. Lütfen API anahtarınızı ve bölgenizi kontrol edin.")
        else:
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = model.generate_content(prompt)
                
                # Yazma efekti (Gerçekçi Jarvis deneyimi)
                for chunk in response.text.split():
                    full_response += chunk + " "
                    time.sleep(0.04)
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"İşlem Kesildi: {e}")








