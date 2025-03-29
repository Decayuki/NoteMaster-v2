import streamlit as st
from st_supabase_connection import SupabaseConnection
import os
import json
import time
from src.config import VERSION

# Initialiser la connexion Supabase
conn = st.connection('supabase', type=SupabaseConnection)
supabase = conn.client

def get_user_session():
    """Récupère la session utilisateur actuelle"""
    try:
        return conn.auth.get_user()
    except Exception:
        return None

def get_redirect_url():
    """Récupère l'URL de redirection configurée"""
    # Utiliser l'URL de l'application Streamlit Cloud si disponible
    if 'REDIRECT_URL' in st.secrets:
        return st.secrets['REDIRECT_URL']
    # Sinon, utiliser l'URL par défaut pour le développement local
    return "http://localhost:8501"

def get_auth_url():
    """Génère une URL d'authentification Google sans afficher d'interface"""
    try:
        # Configurer l'authentification Google
        redirect_url = get_redirect_url()
        
        auth_config = {
            "provider": "google",
            "options": {
                "redirectTo": redirect_url,
                "scopes": "email profile",
                "queryParams": {
                    "access_type": "offline",
                    "prompt": "consent"
                }
            }
        }
        
        # Générer l'URL d'authentification
        auth_response = conn.auth.sign_in_with_oauth(auth_config)
        
        # Vérifier si nous avons une URL
        if hasattr(auth_response, 'url'):
            return auth_response.url
        return None
    except Exception as e:
        print(f"Erreur lors de la génération de l'URL d'authentification: {str(e)}")
        return None

def sign_in_with_google():
    """Initialise la connexion avec Google"""
    try:
        # Vérifier si un code d'autorisation est présent dans l'URL
        code = st.query_params.get("code", None)
        
        if code:
            return handle_auth_callback(code)
        
        # Afficher le bouton de connexion qui redirige vers la page d'authentification séparée
        st.markdown("""
        <div style="text-align: center">
            <h3>🔐 Authentification Google requise</h3>
            <p>Cliquez sur le bouton ci-dessous pour vous connecter avec Google</p>
            <a href="/Auth_Redirect" target="_top">
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
        """, unsafe_allow_html=True)
        
        return None  # On ne renvoie plus l'URL ici
    except Exception as e:
        st.error("❌ Erreur lors de l'authentification")
        st.error(f"Message : {str(e)}")
        import traceback
        st.code(traceback.format_exc(), language="python")
        return None

def handle_auth_callback(code):
    """Gère le callback d'authentification et échange le code contre une session"""
    try:
        # Essayer d'échanger le code contre une session
        session = conn.auth.exchange_code_for_session({
            'auth_code': code
        })
        
        if session:
            st.success("✅ Connexion réussie !")
            # Effacer les paramètres d'URL
            st.query_params.clear()
            # Recharger la page
            st.rerun()
            return True
    except Exception as e:
        st.error(f"❌ Erreur lors de l'échange du code : {str(e)}")
        st.query_params.clear()
    return False

def sign_out():
    """Déconnexion de l'utilisateur"""
    try:
        result = conn.auth.sign_out()
        st.success("✅ Vous avez été déconnecté avec succès !")
        # Nettoyer la session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        return result
    except Exception as e:
        st.error(f"❌ Erreur lors de la déconnexion : {str(e)}")
        return None

def get_user_info():
    """Récupère les informations de l'utilisateur connecté"""
    user_session = get_user_session()
    if not user_session:
        return None
    
    user_data = {
        "id": user_session.user.id,
        "email": user_session.user.email,
        "name": user_session.user.user_metadata.get("full_name", ""),
        "avatar_url": user_session.user.user_metadata.get("avatar_url", ""),
        "provider": "google"
    }
    
    return user_data
