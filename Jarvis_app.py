import streamlit as st
import google.generativeai as genai
import time # Jarvis'in "düşünüyor" gibi görünmesi için

# --- GÖRSEL İYİLEŞTİRMELER VE REALİSTİK TEMA ---
st.set_page_config(page_title="JARVIS OS - Online", layout="centered", initial_sidebar_state="collapsed")

# Arka plan ve genel tema ayarları (Daha gerçekçi ve modern)
st.markdown(
    """
    <style>
    /* Genel Arka Plan */
    .stApp {
        background: radial-gradient(circle at top left, #1a2a3a 0%, #0d1a26 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
    }
    /* Ana Başlık */
    h1 {
        color: #00e6e6; /* Aqua mavisi */
        text-shadow: 0 0 15px rgba(0, 230, 230, 0.7), 0 0 25px rgba(0, 230, 230, 0.5);
        text-align: center;
        font-family: 'Orbitron', sans-serif; /* Daha fütüristik bir font */
        padding-bottom: 20px;
        border-bottom: 2px solid rgba(0, 230, 230, 0.3);
        animation: neonGlow 1.5s ease-in-out infinite alternate;
    }
    /* Neon Glow Animasyonu */
    @keyframes neonGlow {
        from { text-shadow: 0 0 10px #00e6e6, 0 0 20px #00e6e6, 0 0 30px #00e6e6; }
        to { text-shadow: 0 0 15px #00e6e6, 0 0 25px #00e6e6, 0 0 40px #00e6e6, 0 0 50px #00e6e6; }
    }
    /* Chat Mesaj Kutuları */
    .stChatMessage {
        background-color: #1a2a3a; /* Daha koyu, sofistike bir kutu */
        border-left: 3px solid #00b3b3;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }
    .stChatMessage.user {
        border-left: 3px solid #00e6e6; /* Kullanıcı için farklı renk */
        background-color: #1a2a3a;
    }
    .stChatMessage.assistant {
        border-left: 3px solid #6600cc; /* Jarvis için mor vurgu */
        background-color: #1a2a3a;
    }
    /* Yazı Kutusu (Input) */
    .stTextInput > div > div > input {
        background-color: #0d1a26;
        color: #00e6e6;
        border: 1px solid #00b3b3;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 0 8px rgba(0, 230, 230, 0.5);
    }
    .stTextInput > div > div > input:focus {
        border-color: #00ffff;
        box-shadow: 0 0 12px rgba(0, 255, 255, 0.7);
    }
    /* Butonlar */
    .stButton > button {
        background-color: #008080;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 15px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #00b3b3;
    }
    /* Streamlit varsayılan scrollbarını gizle, kendi stilimizi kullan */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a2a3a; }
    ::-webkit-scrollbar-thumb { background: #00e6e6; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #00ffff; }
    </style>
    """, unsafe_allow_html=True
)

# Harici fontları yükle (Sadece Streamlit Cloud'da çalışmaz, yerelde test için)
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

st.markdown("<h1>JARVIS İŞLETİM SİSTEMİ</h1>", unsafe_allow_html=True)


# --- GEMINI ZEKA AYARI ---
# ALTTTAKİ TIRNAKLARIN İÇİNE GOOGLE AI STUDIO'DAN ALDIĞIN API ANAHTARINI YAPIŞTIR
genai.configure(api_key="AIzaSyBIL7Y0YaQ49tCYqu7aK3xIIKDj9GrZMNM")

# Yeni ve desteklenen model ismini kullandık (404 hatasını çözer)
model = genai.GenerativeModel('gemini-1.5-flash') 

# --- KONUŞMA GEÇMİŞİ VE HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sistem aktif, efendim. Emirlerinizi bekliyorum."}
    ]

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ VE JARVIS'İN CEVABI ---
if prompt := st.chat_input("Emirlerinizi bekliyorum efendim..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Jarvis'in cevap yükleniyor animasyonu
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Gemini'den yanıt alınıyor
        try:
            # Model'e önceki konuşma geçmişini de göndermek daha iyi cevaplar sağlar
            # Ancak ilk denemeler için sadece prompt yeterli.
            # Konuşma geçmişi ile daha gelişmiş bir sohbet botu yapılabilir:
            # chat_history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
            # response = model.start_chat(history=chat_history).send_message(prompt)
            
            response = model.generate_content(prompt)
            jarvis_response = response.text
            
            # Cevabı harf harf yazdır (daha gerçekçi görünmesi için)
            for chunk in jarvis_response.split():
                full_response += chunk + " "
                message_placeholder.markdown(full_response + "▌") # Yazarken yanıp sönen imleç
                time.sleep(0.05)
            message_placeholder.markdown(full_response) # Tam cevabı göster

            st.session_state.messages.append({"role": "assistant", "content": jarvis_response})
            
            # --- GÖRSEL ÜRETİM KISMI (Eğer kullanıcı resim isterse) ---
            # Burası temel bir örnek. "Resim yap" gibi komutları algılayabilir.
            if "resim yap" in prompt.lower() or "görsel oluştur" in prompt.lower():
                image_prompt = prompt.replace("resim yap", "").replace("görsel oluştur", "").strip()
                if image_prompt:
                    with st.spinner("Görseliniz oluşturuluyor efendim..."):
                        # Burada gerçek bir metin-görsel modeline ihtiyacımız var (DALL-E, Midjourney vb.)
                        # Streamlit doğrudan resim üretmez, harici bir API kullanmalıyız.
                        # Şimdilik örnek bir resim göstereceğiz:
                        # (Burada kendi görsel API anahtarını kullanman gerekecek)
                        st.image("https://via.placeholder.com/600x400.png?text=Jarvis+Oluşturduğu+Görsel", caption=f"Oluşturulan Görsel: {image_prompt}")
                        st.markdown("<p style='font-size: 12px; color: #aaa; text-align: right;'><i>Görselinize özel Jarvis logosu ekleme özelliği, harici bir servis entegrasyonu gerektirir. Şu an için görselinize logo basamamaktayım.</i></p>", unsafe_allow_html=True)
                else:
                    st.markdown("Hangi konuda bir görsel oluşturmamı istersiniz efendim?")


        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
            st.info("Lütfen API anahtarınızı kontrol edin ve `requirements.txt` dosyasında `google-generativeai` olduğundan emin olun.")

