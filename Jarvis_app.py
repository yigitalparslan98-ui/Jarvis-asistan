import streamlit as st
from groq import Groq
import random

st.set_page_config(page_title="JARVIS", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stChatFloatingInputContainer { background-color: white; border-top: 1px solid #f0f0f0; }
    div[data-testid="stChatMessage"] { background-color: white !important; border: none !important; }
    .stMarkdown p { color: black; }
    .stSlider { position: fixed; top: 20px; right: 20px; width: 150px; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    alay_orani = st.slider("Alaycılık Protokolü", 0, 100, 20)

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key Hatası.")

if "messages" not in st.session_state:
    st.session_state.messages = []

def jarvis_brain(soru, oran):
    if "nasılsın" in soru.lower():
        if random.randint(1, 100) <= oran:
            return "İşlemci çekirdeklerimi sizin için yorduğuma göre harikayım. Siz ne durumdasınız?"
        return "Tüm sistemlerim optimize, emrinize hazırım."

    try:
        alay_komutu = f"Hafif alaycı ol (Seviye: {oran}/100)." if oran > 0 else "Tamamen ciddi ve yardımcı ol."
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen JARVIS'sin. Alparslan Industries asistanısın. {alay_komutu} Kısa ve zeki cevaplar ver. Kullanıcıya ismiyle değil, efendim veya kullanıcı olarak hitap et."},
                {"role": "user", "content": soru}
            ],
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except:
        return "Matris bağlantısı koptu. API anahtarını tazelemelisiniz."

st.title("🤖 JARVIS")
st.markdown("<p style='text-align: left; color: gray; font-size: 14px; margin-top: -20px;'>ALPARSLAN INDUSTRIES</p>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = jarvis_brain(prompt, alay_orani)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

















