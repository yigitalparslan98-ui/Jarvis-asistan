import streamlit as st
from groq import Groq

st.set_page_config(page_title="JARVIS | Alparslan Industries", page_icon="🤖", layout="centered")

# --- CSS: TASARIM VE ANİMASYON ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* DEVASA VE NET BAŞLIK */
    .main-title { 
        font-size: 130px; 
        font-weight: 900; 
        color: #1d1d1f; 
        text-align: center; 
        margin-top: 50px; 
        line-height: 1.0;
        letter-spacing: 15px; /* Harfler arası iyice açıldı */
        text-transform: uppercase;
    }
    
    .sub-title { 
        font-size: 20px; 
        color: #86868b; 
        text-align: center; 
        letter-spacing: 10px; 
        margin-bottom: 60px; 
        font-weight: 500;
    }

    /* ALT PANEL */
    .fixed-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 25px 12%;
        border-top: 1px solid #e5e5e5;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 20px;
    }

    /* WINDOWS SES ORB'U BUTON OLARAK */
    .stButton > button {
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        background: linear-gradient(135deg, #0078d4, #00bcf2) !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(0, 120, 212, 0.6) !important;
        transition: all 0.3s ease !important;
        color: white !important;
        font-size: 24px !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 30px rgba(0, 120, 212, 0.8) !important;
    }

    /* Mesaj Alanı Padding */
    .block-container { padding-bottom: 200px; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM ALTYAPISI ---
client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages = []

def speak_js(text):
    if text:
        clean = text.replace("'", "").replace("\n", " ")
        st.components.v1.html(f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean}'); msg.lang = 'tr-TR'; window.speechSynthesis.speak(msg);</script>", height=0)

def jarvis_brain(soru, oran):
    if not client: return "Bağlantı kesildi."
    alay = f"Sarcastic and honest level {oran}/100." if oran > 30 else "Professional."
    try:
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": f"Sen JARVIS'sin. {alay} Yiğit'e çok kısa ve sesli okunacak şekilde cevap ver."}, {"role": "user", "content": soru}],
            temperature=0.8,
        )
        return compl.choices[0].message.content
    except: return "İşlemci aşırı ısındı Yiğit."

# --- UI ---
alay_orani = st.sidebar.slider("Alaycılık Modu", 0, 100, 20)

st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

# --- ALT PANEL: ORB VE PROMPT ---
with st.container():
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.15, 0.85])
    
    with c1:
        # Mavi Orb burada buton görevi görüyor
        orb_clicked = st.button("🔵") 
        
    with c2:
        with st.form(key='chat_form', clear_on_submit=True):
            u_input = st.text_input("", placeholder="Komutunu yaz veya Orb'a basarak konuş...", label_visibility="collapsed")
            submit = st.form_submit_button("SORGULA", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ÇALIŞTIRMA MANTIĞI ---

# 1. Yazılı Giriş
if u_input or submit:
    if u_input:
        st.session_state.messages.append({"role": "user", "content": u_input})
        res = jarvis_brain(u_input, alay_orani)
        st.session_state.messages.append({"role": "assistant", "content": res})
        speak_js(res)
        st.rerun()

# 2. Orb'a Basınca Dinleme (Sesli Giriş)
if orb_clicked:
    js = """
    <script>
    var rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    rec.lang = 'tr-TR';
    rec.start();
    rec.onresult = function(e) {
        var t = e.results[0][0].transcript;
        var inp = window.parent.document.querySelectorAll('input[type="text"]')[0];
        inp.value = t;
        inp.dispatchEvent(new Event('input', {bubbles: true}));
        inp.dispatchEvent(new Event('change', {bubbles: true}));
    }
    </script>
    """
    st.components.v1.html(js, height=0)
    st.toast("Seni dinliyorum Yiğit...")

























