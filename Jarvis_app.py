import streamlit as st
from datetime import datetime

# 1. Sayfa Yapılandırması
st.set_page_config(page_title="JARVIS OS", layout="centered")

# 2. Havalı Neon Tasarım (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a;
    }
    .stChatMessage {
        background-color: #161b22;
        border-radius: 15px;
        border: 1px solid #00d4ff;
        margin-bottom: 10px;
        color: #00d4ff;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    h1 {
        color: #00d4ff;
        text-align: center;
        text-shadow: 0 0 15px #00d4ff;
        font-family: 'Courier New', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>JARVIS [ SİSTEM AKTİF ]</h1>", unsafe_allow_html=True)

# 3. Sohbet Geçmişi Hafızası
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Eski Mesajları Ekrana Çiz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Alt Kısımdaki Yazı Yazma Kutusu (Chat Input)
prompt = st.chat_input("Jarvis'e bir emir verin...")

if prompt:
    # Senin mesajını ekrana bas ve hafızaya al
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- JARVIS CEVAP MANTIĞI ---
    user_text = prompt.lower()
    
    if "selam" in user_text or "merhaba" in user_text:
        response = "Merhaba efendim, tüm protokoller hazır. Sizi dinliyorum."
    elif "saat" in user_text:
        suan = datetime.now().strftime("%H:%M")
        response = f"Şu an saat tam olarak {suan} efendim."
    elif "sistemi kapat" in user_text:
        response = "Üzgünüm efendim, ana terminal üzerinden yetki verilmedi."
    else:
        response = "Anlaşılamadı efendim, komut veritabanına eklenmemiş."

    # Jarvis'in cevabını ekrana bas ve hafızaya al
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})