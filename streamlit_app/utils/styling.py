import streamlit as st
import os

def load_css():
    """Charge le CSS personnalisé"""
    css_file = "streamlit_app/assets/style.css"
    
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
def apply_custom_styling():
    """Applique le styling personnalisé complet"""
    load_css()
    
    st.markdown("""
        <style>
        /* Additional inline styles */
        .big-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #6b7280;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
