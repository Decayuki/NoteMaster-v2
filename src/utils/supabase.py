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

def sign_in_with_google():
    """Initialise la connexion avec Google"""
    try:
        # Vérifier si un code d'autorisation est présent dans l'URL
        code = st.query_params.get("code", None)
        
        if code:
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
            auth_url = auth_response.url
            
            # Afficher un message d'information avec instructions claires
            st.info(
                "### 🔐 Authentification Google requise\n\n"
                "Pour vous connecter à NoteMaster v{}, suivez ces étapes :\n\n"
                "1. Cliquez sur le bouton ci-dessous pour ouvrir la page de connexion Google\n"
                "2. Connectez-vous avec votre compte Google\n"
                "3. Revenez sur cette page après l'authentification\n"
                "4. Si nécessaire, cliquez sur 'Finaliser la connexion'".format(VERSION),
                icon="ℹ️"
            )
            
            # Utiliser JavaScript pour ouvrir dans un nouvel onglet
            js = f'''function openGoogleAuth() {{ window.open("{auth_url}", "_blank"); }}'''
            
            # Créer un bouton stylisé pour l'authentification
            st.markdown(f'''
                <script>{js}</script>
                <div style="text-align: center; margin: 20px 0;">
                    <button 
                        onclick="openGoogleAuth()" 
                        style="
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
                </div>
                
                <div style="padding: 15px; border: 1px solid #f0f2f6; border-radius: 8px; background-color: #f8f9fa; margin-top: 20px;">
                    <p><strong>⚠️ Important :</strong> Si vous êtes redirigé vers cette page avec une URL contenant <code>code=...</code> :</p>
                    <button 
                        onclick="window.location.href=window.location.href" 
                        style="
                            padding: 8px 16px; 
                            background-color: #4285F4; 
                            color: white; 
                            border: none; 
                            border-radius: 4px; 
                            cursor: pointer; 
                            margin-top: 10px;
                            font-weight: bold;
                        ">
                        Finaliser la connexion
                    </button>
                </div>
            ''', unsafe_allow_html=True)
            
            return auth_url
        else:
            st.error("❌ Impossible d'obtenir l'URL d'authentification")
            return None
        
    except Exception as e:
        st.error("❌ Erreur lors de l'authentification")
        st.error(f"Message : {str(e)}")
        import traceback
        st.code(traceback.format_exc(), language="python")
        return None

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
