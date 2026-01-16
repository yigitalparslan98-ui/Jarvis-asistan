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
<h1>ALPARSLAN INDUSTRIES - JARVIS v3.3</h1>
""", unsafe_allow_html=True)

# --- 2. KOTA KORUMALI MODEL BAĞLANTISI ---
@st.cache_resource
def get_safe_jarvis():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Anahtarı bulunamadı."
        
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # En güncel modeli listeleme yöntemiyle seç
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not available_models: return None, "Model bulunamadı."
        
        instruction = "Sen Jarvis'sin. Alparslan Industries tarafından yapıldın. Her zaman Türkçe konuş ve efendim diye hitap et."
        return genai.GenerativeModel(available_models[0], system_instruction=instruction), None
    except Exception as e:
        return None, str(e)

model, error_msg = get_safe_jarvis()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler aktif. Emirlerinizi bekliyorum efendim."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. AKILLI YANIT SİSTEMİ (429 KORUMALI) ---
if prompt := st.chat_input("Talimatınız nedir?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_resp = ""
        
        if error_msg:
            st.error(f"Sistem Hatası: {error_msg}")
        else:
            try:
                # 429 hatasını önlemek için küçük bir bekleme ekliyoruz
                with st.spinner("İşleniyor..."):
                    response = model.generate_content(prompt)
                    
                for chunk in response.text.split():
                    full_resp += chunk + " "
                    time.sleep(0.04)
                    placeholder.markdown(full_resp + "▌")
                placeholder.markdown(full_resp)
                st.session_state.messages.append({"role": "assistant", "content": full_resp})
                
            except Exception as e:
                # EĞER 429 HATASI ALIRSAK KULLANICIYA ANLATALIM
                if "429" in str(e):
                    st.warning("⚠️ Yoğunluk algılandı efendim. Ücretsiz kota limitine ulaşıldı. Lütfen 30 saniye sonra tekrar deneyin.")
                else:
                    st.error(f"Bir hata oluştu: {e}")














