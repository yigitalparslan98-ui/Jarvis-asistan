import streamlit as st
import google.generativeai as genai
import time

# --- 1. GÖRSEL TASARIM (ALPARSLAN INDUSTRIES ÖZEL TEMASI) ---
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
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        margin-bottom: 15px;
    }
    h1 {
        font-family: 'Courier New', monospace;
        text-align: center;
        text-shadow: 0 0 25px #00f2ff;
        letter-spacing: 5px;
        border-bottom: 2px solid rgba(0, 242, 255, 0.2);
        padding-bottom: 15px;
    }
    .stChatInputContainer {
        border-radius: 30px;
        border: 1px solid #00f2ff !important;
    }
</style>
<h1>ALPARSLAN INDUSTRIES - JARVIS v3.1</h1>
""", unsafe_allow_html=True)

# --- 2. GÜVENLİ API VE MODEL BAĞLANTISI ---
# Not: API Anahtarınızı GitHub'a yazmayın! 
# Streamlit Cloud panelinden Settings > Secrets kısmına ekleyin.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # En güncel modeli doğrudan tanımlıyoruz
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Kritik Hata: API Anahtarı (Secrets) bulunamadı!")
        st.stop()

except Exception as e:
    st.error(f"Sistem Başlatılamadı: {e}")
    st.stop()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Alparslan Industries sistemleri aktif. Hoş geldiniz efendim, emrinizdeyim."}
    ]

# Eski mesajları ekrana yansıt
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ETKİLEŞİM VE YANIT SİSTEMİ ---
if prompt := st.chat_input("Bir komut girin efendim..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jarvis'in Yanıtı
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Yapay zekadan yanıt al
            response = model.generate_content(prompt)
            jarvis_text = response.text
            
            # Kelime kelime yazdırma efekti
            for chunk in jarvis_text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bağlantı Hatası: Lütfen API anahtarınızı veya internetinizi kontrol edin. Hata: {e}")










