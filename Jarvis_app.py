
import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime, timedelta

# --- 1. SAYAÇ VE KOTA KORUMA SINIFI ---
class JarvisSystem:
    def __init__(self):
        self.count = 0
        self.last_request_time = datetime.now() - timedelta(seconds=20)

@st.cache_resource
def get_system():
    return JarvisSystem()

system = get_system()

# --- 2. GÖRSEL TASARIM ---
st.set_page_config(page_title="ALPARSLAN INDUSTRIES | JARVIS", layout="wide")
st.markdown(f"""
<style>
    .stApp {{ background: radial-gradient(circle, #001219 0%, #000000 100%); color: #00f2ff; }}
    h1 {{ font-family: 'Courier New', monospace; text-align: center; text-shadow: 0 0 25px #00f2ff; letter-spacing: 10px; text-transform: uppercase; }}
    .visitor-box {{
        position: fixed; top: 15px; right: 15px; background: rgba(0, 242, 255, 0.1);
        padding: 8px 15px; border-radius: 10px; border: 1px solid #00f2ff;
        font-family: monospace; font-size: 14px; z-index: 1000;
    }}
    .stChatMessage {{ background: rgba(0, 242, 255, 0.07); border: 1px solid rgba(0, 242, 255, 0.3); border-radius: 20px; }}
</style>
<div class="visitor-box">ERİŞİM KAYDI: #{system.count}</div>
<h1>ALPARSLAN INDUSTRIES</h1>
""", unsafe_allow_html=True)

# --- 3. MODEL BAĞLANTISI ---
@st.cache_resource
def init_jarvis():
    try:
        if "GOOGLE_API_KEY" not in st.secrets: return None, "API Key Eksik"
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Mevcut modelleri tara
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        instruction = "Sen Jarvis'sin. Alparslan Industries tarafından yapıldın. Her zaman Türkçe konuş ve efendim diye hitap et."
        return genai.GenerativeModel(models[0], system_instruction=instruction), None
    except Exception as e:
        return None, str(e)

jarvis, err = init_jarvis()

# --- 4. SOHBET PANELİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler aktif efendim. Kota koruma protokolü devrede."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# --- 5. KOMUT İŞLEME VE KOTA KORUMASI ---
if prompt := st.chat_input("Komut bekleniyor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # KOTA KONTROLÜ: Son istek üzerinden 15 saniye geçti mi?
    now = datetime.now()
    seconds_since_last = (now - system.last_request_time).total_seconds()
    
    with st.chat_message("assistant"):
        if err:
            st.error(err)
        elif seconds_since_last < 15:
            wait_time = int(15 - seconds_since_last)
            st.warning(f"⚠️ Sistem yoğunluğu efendim. İşlemcilerin soğuması için {wait_time} saniye bekleyiniz.")
        else:
            placeholder = st.empty()
            full_resp = ""
            try:
                # İstek gönderilmeden önce zamanı güncelle ve sayacı artır
                system.last_request_time = datetime.now()
                system.count += 1
                
                with st.spinner("Analiz ediliyor..."):
                    response = jarvis.generate_content(prompt)
                
                for chunk in response.text.split():
                    full_resp += chunk + " "
                    time.sleep(0.05)
                    placeholder.markdown(full_resp + "▌")
                placeholder.markdown(full_resp)
                st.session_state.messages.append({"role": "assistant", "content": full_resp})
                
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ Google Ücretsiz Kotası Doldu. Lütfen 1 dakika sonra tekrar deneyiniz.")
                else:
                    st.error(f"Sinyal hatası: {e}")

# Sayfa her yüklendiğinde sayacı güncellemek için ufak bir tetikleyici
st.rerun = False














