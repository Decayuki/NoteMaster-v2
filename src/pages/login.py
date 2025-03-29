import streamlit as st
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.supabase import sign_in_with_google, sign_out, get_user_session
from src.config import VERSION

def show_login_page():
    """Affiche la page de connexion"""
    st.title(f"Bienvenue sur NoteMaster v{VERSION}")
    
    # Vérifier si un code d'autorisation est présent dans l'URL
    code = st.query_params.get("code", None)
    if code:
        st.info("🔄 Finalisation de la connexion en cours...")
        sign_in_with_google()
    
    # Vérifier si l'utilisateur est déjà connecté
    user = get_user_session()
    if user:
        st.write(f"Connecté en tant que : {user.user.email}")
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
                    
                    if auth_url:
                        # Bouton de redirection
                        st.markdown(f'''
                            <div style="text-align: center; margin-top: 20px;">
                                <a href="{auth_url}" target="_self">
                                    <button style="
                                        background-color: #4285F4;
                                        color: white;
                                        padding: 10px 20px;
                                        border: none;
                                        border-radius: 5px;
                                        cursor: pointer;
                                        width: 100%;
                                        display: inline-flex;
                                        align-items: center;
                                        justify-content: center;
                                        gap: 10px;
                                        font-family: Arial, sans-serif;
                                        text-decoration: none;
                                    ">
                                        <img src="https://www.google.com/favicon.ico" style="width: 20px; height: 20px;"/>
                                        Continuer vers Google
                                    </button>
                                </a>
                            </div>
                        ''', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("### ❌ Erreur lors de la connexion")
                    st.error(f"Message : {str(e)}")
                    st.error("Détails techniques :")
                    import traceback
                    st.code(traceback.format_exc(), language="python")
        
        # Message d'information
        st.info("""
        En vous connectant avec Google :
        - Accédez à vos notes depuis n'importe quel appareil
        - Gardez une trace de votre progression
        - Synchronisez automatiquement vos données
        """)
