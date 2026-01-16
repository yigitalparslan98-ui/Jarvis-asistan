import streamlit as st
import google.generativeai as genai
import time

# --- 1. YEREL ZİYARETÇİ SAYACI ---
if 'visitor_count' not in st.session_state:
    # Sayfa her sıfırdan yüklendiğinde (yeni kişi geldiğinde) 1 artar
    if 'total_hits' not in st.cache_resource:
        st.cache_resource.total_hits = 0
    st.cache_resource.total_hits += 1
    st.session_state.visitor_count = st.cache_resource.total_hits

# --- 2. GÖRSEL TASARIM ---
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
        top: 10px;
        right: 10px;
        background: rgba(0, 242, 255, 0.1);
        padding: 5px 15px;
        border-radius: 10px;
        border: 1px solid #00f2ff;
        font-family: monospace;
        font-size: 12px;
    }}
    .stChatMessage {{ background: rgba(0, 242, 255, 0.07); border: 1px solid rgba(0, 242, 255, 0.3); border-radius: 20px; }}
</style>
<div class="visitor-box">ERİŞİM KAYDI: #{st.cache_resource.total_hits}</div>
<h1>ALPARSLAN INDUSTRIES</h1>
""", unsafe_allow_html=True)

# --- 3. MODEL BAĞLANTISI ---
@st.cache_resource
def init_jarvis():
    try:
        if "GOOGLE_API_KEY" not in st.secrets: return None, "API Key Eksik"
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        instruction = "Sen Jarvis'sin. Alparslan Industries tarafından yapıldın. Her zaman Türkçe konuş ve efendim diye hitap et."
        return genai.GenerativeModel(models[0], system_instruction=instruction), None
    except Exception as e:
        return None, str(e)

jarvis, err = init_jarvis()

# --- 4. SOHBET ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler aktif. Yerel veri tabanı üzerinden takip başlatıldı efendim."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Komut bekleniyor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        if err: st.error(err)
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
                st.error(f"Hata: {e}")














