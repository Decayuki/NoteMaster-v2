import streamlit as st
import sys
import os
import json

def main():
    # Configuration de base de Streamlit
    st.set_page_config(
        page_title="NoteMaster",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Ajouter un bouton de débogage pour afficher les informations de session
    with st.sidebar:
        if st.button("Afficher détails de session"):
            try:
                from src.utils.supabase import conn
                session = conn.auth.get_session()
                st.json(session)
            except Exception as e:
                st.error(f"Erreur: {e}")
    
    # Vérifier si un token est présent dans l'URL
    token = st.query_params.get("token", None)
    if token:
        st.info("🔄 Finalisation de la connexion en cours...")
        try:
            # Valider le token et créer une session
            from src.utils.supabase import validate_token
            if validate_token(token):
                # Effacer le token de l'URL pour la sécurité
                st.query_params.clear()
                # Recharger la page pour montrer le tableau de bord
                st.rerun()
            else:
                st.error("❌ Token invalide ou expiré")
                # Nettoyer l'URL
                st.query_params.clear()
        except Exception as e:
            st.error(f"❌ Erreur lors de la validation du token: {str(e)}")
            import traceback
            st.code(traceback.format_exc(), language="python")
            # Nettoyage des paramètres pour éviter une boucle
            st.query_params.clear()
    
    # Vérifier si l'utilisateur est déjà connecté
    from src.utils.supabase import get_user_session
    user_session = get_user_session()
    
    if user_session:
        # Afficher les informations de base de l'utilisateur
        st.sidebar.success(f"Connecté en tant que: {user_session.user.email}")
        # Rediriger vers le tableau de bord
        from src.pages.dashboard import show_dashboard
        show_dashboard()
        return

    # Afficher le formulaire de connexion
    st.title("📚 NoteMaster - Votre assistant d'études")
    
    # Section de connexion
    with st.container():
        st.subheader("🔐 Connexion")
        st.write("Connectez-vous avec votre compte Google pour accéder à vos notes et quiz.")
        
        # URL de la page d'authentification externe
        auth_page_url = "https://decayuki.github.io/notemaster-auth/"
        
        # Créer un bouton qui ouvre la page d'authentification externe
        st.markdown(f"""
        <div style="text-align: center">
            <a href="{auth_page_url}" target="_blank">
                <button style="
                    background-color: #4285F4;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                ">
                    <img src="https://www.google.com/favicon.ico" style="width: 20px; height: 20px;"/>
                    Se connecter avec Google
                </button>
            </a>
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <p>Cette authentification contourne le problème d'iframe de Streamlit Cloud.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Comment ça fonctionne
    with st.expander("🔍 Comment fonctionne cette authentification"):
        st.write("""
        Cette méthode d'authentification utilise une page externe hébergée sur GitHub Pages pour:
        
        1. Contourner les limitations d'iframe de Streamlit Cloud
        2. Gérer l'authentification Google de manière sécurisée
        3. Obtenir un token d'accès validé par Supabase
        4. Vous rediriger vers cette application avec le token
        
        C'est une approche recommandée pour les applications Streamlit en production.
        """)
    
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
