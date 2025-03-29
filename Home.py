import streamlit as st
import sys
import os

def main():
    # Configuration de base de Streamlit
    st.set_page_config(
        page_title="NoteMaster",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Vérifier si un code d'autorisation est présent dans l'URL
    code = st.query_params.get("code", None)
    if code:
        st.info("🔄 Finalisation de la connexion en cours...")
        from src.utils.supabase import handle_auth_callback
        handle_auth_callback(code)
        # Recharger la page sans les paramètres
        st.rerun()
    
    # Vérifier si l'utilisateur est déjà connecté
    from src.utils.supabase import get_user_session
    user_session = get_user_session()
    
    if user_session:
        # Rediriger vers le tableau de bord
        from src.pages.dashboard import show_dashboard
        show_dashboard()
        return

    # Style personnalisé
    st.markdown("""
        <style>
            .stButton button {
                width: 100%;
                background-color: #4285F4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            .main {
                background-color: #0E1117;
            }
            .st-emotion-cache-18ni7ap {
                background-color: #262730;
            }
            .stAlert {
                background-color: #262730;
                color: white;
            }
            .stExpander {
                background-color: #262730;
                border: 1px solid #4285F4;
                border-radius: 5px;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    try:
        # Importer la version
        from src.config import VERSION
        
        # En-tête avec version
        st.title(f"Bienvenue sur NoteMaster v{VERSION}")
        st.write("Connectez-vous pour accéder à vos notes")
        
        # Bouton de connexion Google
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Se connecter avec Google", type="primary", use_container_width=True):
                try:
                    # Ajouter le répertoire src au PYTHONPATH
                    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
                    sys.path.append(src_path)
                    
                    from src.utils.supabase import sign_in_with_google
                    
                    auth_url = sign_in_with_google()
                    if auth_url:
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
                    st.error("Stack trace :")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Message d'information
        st.info("""
            En vous connectant avec Google :
            - Accédez à vos notes depuis n'importe quel appareil
            - Gardez une trace de votre progression
            - Synchronisez automatiquement vos données
        """)
        
    except Exception as e:
        st.error("### ❌ Erreur lors du chargement de l'application")
        st.error(f"Message : {str(e)}")
        st.error("Stack trace :")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
