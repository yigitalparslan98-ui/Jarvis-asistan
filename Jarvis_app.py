import streamlit as st
import google.generativeai as genai
import time

# --- 1. GİZLİLİK ODAKLI SAYAÇ SİSTEMİ ---
# Streamlit'te veriyi güvenli bir şekilde önbelleğe almak için bu sınıfı kullanıyoruz
class Counter:
    def __init__(self):
        self.count = 0

@st.cache_resource
def get_counter():
    return Counter()

counter = get_counter()
counter.count += 1

# --- 2. GÖRSEL TASARIM (ALPARSLAN INDUSTRIES) ---
st.set_page_config(page_title="ALPARSLAN INDUSTRIES | JARVIS", layout="wide")

st.markdown(f"""
<style>
    .stApp {{ background: radial-gradient(circle, #001219 0%, #000000 100%); color: #00f2ff; }}
    h1 {{ 
        font-family: 'Courier New', monospace; 
        text-align: center; 
        text-shadow: 0 0 25px #00f2ff; 
        letter-spacing: 10px;
        text-transform: uppercase;
    }}
    .visitor-box {{
        position: fixed;
        top: 15px;
        right: 15px;
        background: rgba(0, 242, 255, 0.1);
        padding: 8px 15px;
        border-radius: 10px;
        border: 1px solid #00f2ff;
        font-family: monospace;
        font-size: 14px;
        z-index: 1000;
    }}
    .stChatMessage {{ background: rgba(0, 242, 255, 0.07); border: 1px solid rgba(0, 242, 255, 0.3); border-radius: 20px; }}
</style>
<div class="visitor-box">ERİŞİM KAYDI: #{counter.count}</div>
<h1>ALPARSLAN INDUSTRIES</h1>
""", unsafe_allow_html=True)

# --- 3. MODEL BAĞLANTISI ---
@st.cache_resource
def init_jarvis():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Anahtarı bulunamadı (Secrets'ı kontrol edin)."
        
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # Mevcut modelleri listele ve ilkini seç
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return None, "Kullanılabilir model bulunamadı."
            
        instruction = "Sen Jarvis'sin. Alparslan Industries tarafından yapıldın. Her zaman Türkçe konuş ve efendim diye hitap et."
        return genai.GenerativeModel(available_models[0], system_instruction=instruction), None
    except Exception as e:
        return None, str(e)

jarvis, err = init_jarvis()

# --- 4. SOHBET PANELİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler aktif. Yerel erişim kaydı oluşturuldu. Emrinizdeyim efendim."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"])

if prompt := st.chat_input("Komut bekleniyor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        if err:
            st.error(err)
        else:
            placeholder = st.empty()
            full_resp = ""
            try:
                response = jarvis.generate_content(prompt)
                for chunk in response.text.split():
                    full_resp += chunk + " "
                    time.sleep(0.04)
                    placeholder.markdown(full_resp + "▌")
                placeholder.markdown(full_resp)
                st.session_state.messages.append({"role": "assistant", "content": full_resp})
            except Exception as e:
                st.error(f"Sinyal hatası: {e}")














