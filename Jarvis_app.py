import streamlit as st
import google.generativeai as genai
import time

# --- 1. GÖRSEL TASARIM (ALPARSLAN INDUSTRIES) ---
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
        letter-spacing: 5px;
        border-bottom: 2px solid rgba(0, 242, 255, 0.2);
    }
</style>
<h1>ALPARSLAN INDUSTRIES - JARVIS v3.1</h1>
""", unsafe_allow_html=True)

# --- 2. AKILLI MODEL BAĞLANTISI ---
@st.cache_resource
def power_up_jarvis():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "Kritik Hata: API Anahtarı Streamlit Secrets içinde bulunamadı!"
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Denenecek model isimleri (Google'ın kabul ettiği tüm varyasyonlar)
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
        
        last_error = ""
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # Küçük bir test çalıştırması yapıyoruz
                test_response = model.generate_content("ping")
                if test_response:
                    return model, None
            except Exception as e:
                last_error = str(e)
                continue
        
        return None, f"Hiçbir model çalıştırılamadı. Son hata: {last_error}"
        
    except Exception as e:
        return None, f"Sistem başlatma hatası: {str(e)}"

# Jarvis'i uyandır
jarvis_model, error_msg = power_up_jarvis()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Alparslan Industries sistemleri aktif. Hoş geldiniz efendim, emrinizdeyim."}
    ]

# Mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KOMUT SİSTEMİ ---
if prompt := st.chat_input("Bir komut girin efendim..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if error_msg:
            st.error(error_msg)
            st.info("Lütfen Google AI Studio'dan 'Create API key in NEW project' diyerek yeni bir anahtar alın.")
        elif jarvis_model:
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = jarvis_model.generate_content(prompt)
                # Yazma efekti
                for chunk in response.text.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Yanıt oluşturulamadı: {e}")











