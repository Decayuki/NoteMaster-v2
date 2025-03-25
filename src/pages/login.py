import streamlit as st
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.supabase import sign_in_with_google, sign_out

def show_login_page():
    """Affiche la page de connexion"""
    st.title("Bienvenue sur NoteMaster")
    
    # Vérifier si l'utilisateur est déjà connecté
    if "user" in st.session_state:
        st.write(f"Connecté en tant que : {st.session_state.user.email}")
        if st.button("Se déconnecter"):
            try:
                sign_out()
                st.session_state.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de la déconnexion : {str(e)}")
    else:
        st.write("Connectez-vous pour accéder à vos notes")
        
        # Bouton de connexion Google
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Se connecter avec Google", type="primary", use_container_width=True):
                try:
                    auth_url = sign_in_with_google()
                    st.info("Redirection vers Google...")
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Erreur lors de l'initialisation de la connexion Google : {str(e)}")
                    st.error("Détails de l'erreur :")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Message d'information
        st.info("""
        En vous connectant avec Google :
        - Accédez à vos notes depuis n'importe quel appareil
        - Gardez une trace de votre progression
        - Synchronisez automatiquement vos données
        """)
