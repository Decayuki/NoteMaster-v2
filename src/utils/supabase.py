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
        
        st.write(f"Debug - URL de redirection : {redirect_url}")
        
        # Initialiser la connexion Google
        auth_response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_url,
                "queryParams": {
                    "access_type": "offline",
                    "prompt": "consent"
                }
            }
        })
        
        st.write("Debug - Réponse de l'authentification :")
        st.json(auth_response)
        
        return auth_response.url
        
    except Exception as e:
        st.error(f"Erreur lors de l'initialisation de Google Auth : {str(e)}")
        raise e

def sign_out():
    """Déconnexion de l'utilisateur"""
    return supabase.auth.sign_out()
