import streamlit as st
from groq import Groq

st.set_page_config(page_title="JARVIS | Alparslan Industries", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-title { 
        font-size: 110px; 
        font-weight: 900; 
        color: #f5f5f7 !important; 
        text-align: center; 
        margin-top: 50px; 
        letter-spacing: 12px; 
        text-transform: uppercase;
    }
    
    .sub-title { 
        font-size: 18px; 
        color: #86868b !important; 
        text-align: center; 
        letter-spacing: 8px; 
        margin-bottom: 60px; 
        font-weight: 500;
    }

    .stSlider {
        position: fixed;
        top: 20px;
        right: 30px;
        width: 200px;
        z-index: 10000;
        background: rgba(28, 28, 30, 0.9);
        padding: 15px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        color: white;
    }

    div[data-testid="stChatMessage"] { 
        background-color: #1c1c1e !important; 
        color: #f5f5f7 !important; 
        border-radius: 18px !important; 
        border: 1px solid #38383a !important;
        padding: 18px !important; 
        margin-bottom: 12px !important;
    }

    .fixed-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(20px);
        padding: 15px 12%;
        border-top: 1px solid #38383a;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .stButton > button {
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        background: linear-gradient(135deg, #0078d4, #00bcf2) !important;
        border: none !important;
        box-shadow: 0 0 12px rgba(0, 120, 212, 0.5) !important;
        color: white !important;
    }

    .block-container { padding-bottom: 200px; }
    </style>
    """, unsafe_allow_html=True)

client = None
if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        client = None

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

def speak_js(text):
    if text:
        clean = text.replace("'", "").replace("\n", " ")
        js = f"""
        <script>
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{clean}');
        msg.lang = 'tr-TR';
        msg.rate = 0.85;
        msg.pitch = 0.75;
        window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js, height=0)

def jarvis_brain(soru, oran):
    if not client:
        return "Sinyal yok."
    alay = f"Sarcastic level {oran}/100. Be professional and honest."
    try:
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Sen JARVIS'sin. {alay} Asla isim kullanma. Çok kısa ve öz cevap ver."},
                {"role": "user", "content": soru}
            ],
            temperature=0.8,
        )
        return compl.choices[0].message.content
    except:
        return "API hatası."

alay_orani = st.slider("Alaycılık Seviyesi", 0, 100, 20)

st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

with st.container():
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.1, 0.9])
    
    with c1:
        voice_trigger = st.button("🔵")
        
    with c2:
        with st.form(key='chat_form', clear_on_submit=True):
            u_input = st.text_input("", placeholder="Komutunuzu yazın...", label_visibility="collapsed")
            submit = st.form_submit_button("GÖNDER", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if submit and u_input:
    st.session_state.messages.append({"role": "user", "content": u_input})
    res = jarvis_brain(u_input, alay_orani)
    st.session_state.messages.append({"role": "assistant", "content": res})
    st.session_state.last_response = res
    st.rerun()

if voice_trigger and st.session_state.last_response:
    speak_js(st.session_state.last_response)






























