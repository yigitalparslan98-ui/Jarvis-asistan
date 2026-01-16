import streamlit as st
import google.generativeai as genai
import time

# --- 1. GÖRSEL TASARIM ---
st.set_page_config(page_title="ALPARSLAN INDUSTRIES | JARVIS", layout="wide")
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle, #001219 0%, #000000 100%); color: #00f2ff; }
    .stChatMessage { background: rgba(0, 242, 255, 0.07); border: 1px solid rgba(0, 242, 255, 0.3); border-radius: 20px; }
    h1 { font-family: 'Courier New', monospace; text-align: center; text-shadow: 0 0 25px #00f2ff; border-bottom: 2px solid rgba(0, 242, 255, 0.2); }
</style>
<h1>ALPARSLAN INDUSTRIES - JARVIS v3.1</h1>
""", unsafe_allow_html=True)

# --- 2. %100 ÇALIŞAN OTOMATİK MODEL BULUCU ---
@st.cache_resource
def get_auto_jarvis():
    try:
        # API Anahtarını al
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Anahtarı (Secrets) girilmemiş."
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # MANUEL İSİM YAZMIYORUZ!
        # Google'a soruyoruz: "Bu anahtarla hangi modelleri kullanabilirim?"
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Eğer hiç model bulamazsa
        if not available_models:
            return None, "Bu API anahtarının yetkili olduğu hiçbir model bulunamadı (Google Hesabınızı kontrol edin)."

        # Bulduğu İLK çalışan modeli seçer (Genelde models/gemini-pro veya flash olur)
        secilen_model = available_models[0] 
        final_model = genai.GenerativeModel(secilen_model)
        
        return final_model, None

    except Exception as e:
        return None, f"Bağlantı Hatası: {str(e)}"

# Jarvis'i Başlat
model, error_message = get_auto_jarvis()

# --- 3. SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Alparslan Industries sistemleri aktif. Emrinizdeyim."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Komut girin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if error_message:
            st.error(error_message)
            st.info("Lütfen Google AI Studio'dan yeni bir anahtar alıp Secrets kısmına ekleyin.")
        elif model:
            placeholder = st.empty()
            full_resp = ""
            try:
                response = model.generate_content(prompt)
                for chunk in response.text.split():
                    full_resp += chunk + " "
                    time.sleep(0.05)
                    placeholder.markdown(full_resp + "▌")
                placeholder.markdown(full_resp)
                st.session_state.messages.append({"role": "assistant", "content": full_resp})
            except Exception as e:
                st.error(f"Hata: {e}")












