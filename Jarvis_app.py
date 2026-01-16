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

# --- 2. EN GÜÇLÜ BAĞLANTI YÖNTEMİ ---
@st.cache_resource
def load_jarvis():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return None, "API Anahtarı bulunamadı."
        
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # 404 HATASINI AŞMAK İÇİN SÜRÜMSÜZ VE EN TEMEL MODELİ ÇAĞIRIYORUZ
        # Google bazen 'models/' takısını zorunlu tutar bazen yasaklar.
        # Burada en geniş kapsamlı olanı seçiyoruz.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test mesajı (Eğer burada hata verirse diğerine geçecek)
        try:
            model.generate_content("Hi")
            return model, None
        except:
            # Yedek model (Eski ama en kararlı olan)
            model = genai.GenerativeModel('gemini-1.0-pro')
            return model, None
            
    except Exception as e:
        return None, str(e)

jarvis, error = load_jarvis()

# --- 3. CHAT SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Alparslan Industries sistemleri aktif. Sizi dinliyorum efendim."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Komut bekleniyor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if error:
            st.error(f"Sistem Hatası: {error}")
        else:
            placeholder = st.empty()
            full_text = ""
            try:
                # Burası 404 hatasını tamamen aşmak için stream=False kullanır
                response = jarvis.generate_content(prompt)
                full_text = response.text
                
                # Jarvis yazma efekti
                displayed_text = ""
                for char in full_text:
                    displayed_text += char
                    placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.01)
                placeholder.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            except Exception as e:
                st.error(f"Yanıt alınamadı: {e}")











