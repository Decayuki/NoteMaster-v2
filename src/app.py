import streamlit as st
import sys
import os

# Ajouter le répertoire courant au PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.login import show_login_page
from pages.notes import show_notes_page
from pages.quiz import show_quiz_page
from utils.supabase import get_user_session
from streamlit_config import configure_streamlit

# Configuration de l'application
APP_NAME = "NoteMaster"
VERSION = "2.0.0"

# Configurer Streamlit
configure_streamlit()

def main():
    """Point d'entrée principal de l'application"""
    
    # Vérifier la session utilisateur
    session = get_user_session()
    
    if not session:
        show_login_page()
    else:
        # Stocker les informations utilisateur dans la session
        st.session_state.user = session.user
        
        # Sidebar avec navigation
        with st.sidebar:
            st.title(f"{APP_NAME} v{VERSION}")
            st.write(f"👤 {st.session_state.user.email}")
            
            # Menu de navigation
            selected = st.radio(
                "Navigation",
                ["📝 Mes Notes", "❓ Quiz", "📊 Statistiques"],
                index=0
            )
        
        # Afficher la page sélectionnée
        if selected == "📝 Mes Notes":
            show_notes_page()
        elif selected == "❓ Quiz":
            show_quiz_page()
        else:
            st.title("📊 Mes Statistiques")
            # TODO: Implémenter les statistiques

if __name__ == "__main__":
    main()
