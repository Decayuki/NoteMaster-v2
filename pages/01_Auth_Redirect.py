import streamlit as st
import os
from src.utils.supabase import get_auth_url

# Configuration de la page
st.set_page_config(
    page_title="NoteMaster - Authentification",
    page_icon="🔐",
    initial_sidebar_state="collapsed"
)

# Masquer le menu Streamlit et la barre latérale
hide_elements = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.css-1d391kg {visibility: hidden;}
</style>
"""
st.markdown(hide_elements, unsafe_allow_html=True)

# Obtenir l'URL d'authentification
auth_url = get_auth_url()

if auth_url:
    # Redirection automatique via HTML
    html_redirect = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url={auth_url}" />
        <title>Redirection vers Google</title>
    </head>
    <body>
        <h1>Redirection vers Google pour authentification...</h1>
        <p>Si vous n'êtes pas redirigé automatiquement, cliquez sur <a href="{auth_url}">ce lien</a>.</p>
    </body>
    </html>
    """
    st.components.v1.html(html_redirect, height=500)
else:
    st.error("Impossible de générer l'URL d'authentification. Veuillez réessayer.")
