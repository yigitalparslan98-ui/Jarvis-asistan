import streamlit as st
from groq import Groq
import random

st.set_page_config(page_title="JARVIS | Alparslan Industries", page_icon="🤖", layout="centered")

# --- CSS İLE ZORLA SABİTLEME ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Başlık Ayarları */
    .main-title { font-size: 65px; font-weight: 900; color: #1d1d1f; text-align: center; margin-top: 50px; letter-spacing: -2px; }
    .sub-title { font-size: 16px; color: #86868b; text-align: center; letter-spacing: 3px; margin-bottom: 100px; font-weight: 500; }
    
    /* Mesaj Kutuları */
    div[data-testid="stChatMessage"] { 
        background-color: #f5f5f7 !important; border-radius: 18px !important; 
        padding: 18px !important; margin-bottom: 12px !important; border: none !important;
    }

    /* ALT PANELİ ZORLA SABİTLEME (THE ANCHOR) */
    .fixed-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 20px 10%;
        border-top: 1px solid #e5e5e5;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Sayfanın altına boşluk bırak ki mesajlar panelin altında kalmasın */
    .main-content { margin-bottom: 150px; }
    </style>
    """, unsafe_allow_html=True)

# --- SİSTEM AYARLARI ---
client = None
if "GROQ_API_KEY" in st.secrets:
    try: client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except: client = None

if "messages" not in st.session_state: st.session_state.messages = []
if "temp_input" not in st.session_state: st.session_state.temp_input = ""

# --- FONKSİYONLAR ---
def speak_js(text):
    if text:
        clean = text.replace("'", "").replace("\n", " ")
        st.components.v1.html(f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean}'); msg.lang = 'tr-TR'; window.speechSynthesis.speak(msg);</script>", height=0)

def jarvis_brain(soru, oran):
    if not client: return "Sinyal yok."
    alay = f"Alaycı ol (Seviye: {oran}/100)." if oran > 30 else "Profesyonel ol."
    try:
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": f"Sen JARVIS'sin. {alay} Kısa cevap ver."}, {"role": "user", "content": soru}],
            temperature=0.7,
        )
        return compl.choices[0].message.content
    except: return "Hata."

# --- ARAYÜZ AKIŞI ---

# Slider (Sağ Üst)
st.markdown("""
<style>
div[data-testid="stSlider"] { position: fixed; top: 20px; right: 20px; width: 200px; z-index: 10000; background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)
alay_orani = st.slider("Alaycılık", 0, 100, 20)

# Başlıklar
st.markdown('<p class="main-title">JARVIS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ALPARSLAN INDUSTRIES</p>', unsafe_allow_html=True)

# Mesaj Geçmişi
st.markdown('<div class="main-content">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# --- EN ALTTAKİ SABİT PANEL ---
with st.container():
    # Bu HTML bloğu paneli en alta sabitler
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        # Enter'a basınca tetiklenmesi için form kullanıyoruz
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("", placeholder="Komut verin...", label_visibility="collapsed")
            submit_button = st.form_submit_button("GÖNDER", use_container_width=True)
            
    with col2:
        # Mikrofon butonu (JS Tetikleyicisi)
        # Not: Streamlit butonları sayfa yeniler, bu yüzden sadece görsel/işlevsel bir JS butonu eklemek daha iyidir ama şimdilik native buton kullanalım.
        mic_pressed = st.button("🎙️", help="Sesli komut (Beta)")

    st.markdown('</div>', unsafe_allow_html=True)

# --- İŞLEM MANTIĞI ---

# Eğer form gönderildiyse
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    res = jarvis_brain(user_input, alay_orani)
    st.session_state.messages.append({"role": "assistant", "content": res})
    speak_js(res)
    st.rerun()

# Mikrofon Mantığı (JS Enjeksiyonu)
if mic_pressed:
    js_code = """
    <script>
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'tr-TR';
    recognition.start();
    recognition.onresult = function(event) {
        var transcript = event.results[0][0].transcript;
        // Streamlit text input'u bul ve doldur
        var inputs = window.parent.document.querySelectorAll('input[type="text"]');
        for (var i = 0; i < inputs.length; i++) {
             if (!inputs[i].disabled) {
                 inputs[i].value = transcript;
                 inputs[i].dispatchEvent(new Event('input', {bubbles: true}));
                 inputs[i].dispatchEvent(new Event('change', {bubbles: true}));
                 // Otomatik gönderim için Enter tuşunu simüle etmeye çalışabiliriz ama zordur.
                 break;
             }
        }
    }
    </script>
    """
    st.components.v1.html(js_code, height=0)
    st.toast("Dinleniyor... Konuşun!")























