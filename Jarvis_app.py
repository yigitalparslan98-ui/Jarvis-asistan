import streamlit as st
from groq import Groq

st.set_page_config(page_title="JARVIS | Alparslan Industries", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-title { 
        font-size: 110px; 
        font-weight: 900; 
        color: #1d1d1f; 
        text-align: center; 
        margin-top: 50px; 
        letter-spacing: 12px; 
        text-transform: uppercase;
    }
    
    .sub-title { 
        font-size: 18px; 
        color: #86868b; 
        text-align: center; 
        letter-spacing: 8px; 
        margin-bottom: 60px; 
        font-weight: 500;
    }

    .fixed-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 15px 12%;
        border-top: 1px solid #e5e5e5;
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
        box-shadow: 0 0 12px rgba(0, 120, 212, 0.3) !important;
        transition: all 0.2s ease !important;
        color: white !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(0, 120, 212, 0.6) !important;
    }

    .block-container { padding-bottom: 180px; }
    </style>
    """, unsafe_allow_html=True)

client = None
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages = []
if "last_response" not in st.session_state: st.session_state.last_response = ""

def speak_js(text):



























