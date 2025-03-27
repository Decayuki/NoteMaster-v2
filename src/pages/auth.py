import streamlit as st
from src.utils.supabase import handle_auth_callback

# Gérer le retour de l'authentification Google
handle_auth_callback()

# Rediriger vers la page principale
st.switch_page("app.py")
