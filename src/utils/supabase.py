from supabase import create_client
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Créer le client Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_session():
    """Récupère la session utilisateur actuelle"""
    return supabase.auth.get_session()

def sign_in_with_google():
    """Initialise la connexion avec Google"""
    import streamlit as st
    
    try:
        # Détecter si nous sommes sur Streamlit Cloud ou en local
        is_cloud = os.getenv('HOSTNAME', '').endswith('streamlit.app')
        redirect_url = "https://notemaster-v2-jkvg9zktfpwttpjuxzwcpe.streamlit.app" if is_cloud else "http://localhost:8501"
        
        # Initialiser la connexion Google
        auth_url = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirectTo": redirect_url,  # Notez le changement de redirect_to à redirectTo
                "skipBrowserRedirect": True  # Important : empêche la redirection automatique
            }
        }).url
        
        st.write("Debug - URL d'authentification :")
        st.code(auth_url)
        
        return auth_url
        
    except Exception as e:
        st.error(f"Erreur lors de l'initialisation de Google Auth : {str(e)}")
        st.error("Détails de l'erreur :")
        import traceback
        st.code(traceback.format_exc())
        raise e

def sign_out():
    """Déconnexion de l'utilisateur"""
    return supabase.auth.sign_out()
