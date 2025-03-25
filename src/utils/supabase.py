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
    import json
    
    try:
        # Détecter si nous sommes sur Streamlit Cloud
        is_cloud = os.getenv('HOSTNAME', '').endswith('streamlit.app')
        os.environ['IS_STREAMLIT_CLOUD'] = 'true' if is_cloud else 'false'
        
        # Importer la configuration
        from src.config import get_redirect_url, get_auth_redirect_url, get_auth_callback_url
        base_url = get_redirect_url()
        redirect_url = get_auth_redirect_url()
        callback_url = get_auth_callback_url()
        
        st.write("### Débogage de la connexion Google")
        st.write("Configuration :")
        st.json({
            "is_cloud": is_cloud,
            "base_url": base_url,
            "redirect_url": redirect_url,
            "callback_url": callback_url,
            "supabase_url": SUPABASE_URL,
            "has_supabase_key": bool(SUPABASE_KEY)
        })
        
        # Initialiser la connexion Google
        auth_config = {
            "provider": "google",
            "options": {
                "redirectTo": redirect_url,
                "queryParams": {
                    "access_type": "offline",
                    "prompt": "consent"
                }
            }
        }
        
        st.write("Configuration de l'authentification :")
        st.json(auth_config)
        
        auth_response = supabase.auth.sign_in_with_oauth(auth_config)
        
        st.write("Réponse de Supabase :")
        st.json({
            "has_url": hasattr(auth_response, 'url'),
            "url": getattr(auth_response, 'url', None),
            "response_type": str(type(auth_response)),
            "response_dict": auth_response.__dict__ if hasattr(auth_response, '__dict__') else str(auth_response)
        })
        
        # Vérifier la réponse
        if not hasattr(auth_response, 'url') or not auth_response.url:
            raise Exception("L'URL d'authentification est manquante dans la réponse")
            
        st.success("URL d'authentification générée avec succès")
        return auth_response.url
        
    except Exception as e:
        st.error("### Erreur lors de l'authentification Google")
        st.error(f"Message d'erreur : {str(e)}")
        st.error("Stack trace :")
        import traceback
        st.code(traceback.format_exc())
        
        # Vérifier l'environnement
        st.error("Variables d'environnement :")
        st.json({
            "SUPABASE_URL exists": bool(os.getenv("SUPABASE_URL")),
            "SUPABASE_KEY exists": bool(os.getenv("SUPABASE_KEY")),
            "HOSTNAME": os.getenv("HOSTNAME", "non défini"),
            "PORT": os.getenv("PORT", "non défini"),
            "IS_STREAMLIT_CLOUD": os.getenv("IS_STREAMLIT_CLOUD", "non défini")
        })
        
        raise e

def sign_out():
    """Déconnexion de l'utilisateur"""
    return supabase.auth.sign_out()
