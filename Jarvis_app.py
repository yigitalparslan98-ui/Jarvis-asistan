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
<h1>ALPARSLAN INDUSTRIES - JARVIS v3.2 (TR)</h1>
""", unsafe_allow_html=True)

# --- 2. TÜRKÇE JARVIS MOTORU ---
@st.cache_resource
def get_turkish_jarvis():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Anahtarı bulunamadı."
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Kullanılabilir modeli bul
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if not available_models:
            return None, "Model bulunamadı."

        secilen_model = available_models[0]
        
        # --- BURASI KRİTİK NOKTA: DİL AYARI ---
        # Modele kim olduğunu ve Türkçe konuşması gerektiğini beynine kazıyoruz.
        jarvis_instruction = """
        Sen Alparslan Industries tarafından geliştirilmiş 'Jarvis' adında gelişmiş bir yapay zekasın.
        Görevin: Kullanıcıya her zaman yardımcı olmak.
        Kural 1: HER ZAMAN TÜRKÇE KONUŞ.
        Kural 2: Kullanıcıya 'efendim' diye hitap et.
        Kural 3: Cevapların net, zeki ve çözüm odaklı olsun.
        """
        
        final_model = genai.GenerativeModel(
            secilen_model,
            system_instruction=jarvis_instruction
        )
        
        return final_model, None

    except Exception as e:
        return None, f"Hata: {str(e)}"

# Jarvis'i Başlat
model, error_message = get_turkish_jarvis()

# --- 3. SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sistemler aktif. Emirlerinizi bekliyorum efendim."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Talimatınız nedir efendim?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if error_message:
            st.error(error_message)
        elif model:
            placeholder = st.empty()
            full_resp = ""
            try:
                # Sohbet geçmişini modele göndermiyoruz, sadece son soruyu yanıtlıyor
                # (Hafıza sorunu yaşamamak için şimdilik en temizi bu)
                response = model.generate_content(prompt)
                
                for chunk in response.text.split():
                    full_resp += chunk + " "
                    time.sleep(0.05)
                    placeholder.markdown(full_resp + "▌")
                placeholder.markdown(full_resp)
                st.session_state.messages.append({"role": "assistant", "content": full_resp})
            except Exception as e:
                st.error(f"İletişim hatası: {e}")













