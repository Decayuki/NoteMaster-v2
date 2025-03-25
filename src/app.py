import streamlit as st
import sys
import os

# Ajouter le répertoire src au PYTHONPATH
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(src_path)

from pages.login import show_login_page
from pages.notes import show_notes_page
from pages.quiz import show_quiz_page
from utils.supabase import get_user_session
from streamlit_config import configure_streamlit

# Débogage des chemins
st.write("### Débogage des chemins")
st.json({
    "PYTHONPATH": sys.path,
    "src_path": src_path,
    "current_dir": os.getcwd(),
    "files_in_src": os.listdir(src_path) if os.path.exists(src_path) else "src n'existe pas"
})

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
