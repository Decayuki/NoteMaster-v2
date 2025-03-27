import streamlit as st
from st_supabase_connection import SupabaseConnection
from urllib.parse import parse_qs

# Initialiser la connexion Supabase
conn = st.connection('supabase', type=SupabaseConnection)
supabase = conn.client

def get_user_session():
    """Récupère la session utilisateur actuelle"""
    try:
        return conn.auth.get_user()
    except Exception:
        return None

def extract_session_from_url():
    """Extrait les informations de session de l'URL"""
    try:
        fragment = st.query_params.get('fragment', None)
        if fragment:
            params = parse_qs(fragment)
            if 'access_token' in params and 'refresh_token' in params:
                return {
                    'access_token': params['access_token'][0],
                    'refresh_token': params['refresh_token'][0],
                    'expires_in': params.get('expires_in', [None])[0],
                    'token_type': params.get('token_type', [None])[0]
                }
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des paramètres : {str(e)}")
    return None

def handle_auth_callback():
    """Gère le retour de l'authentification Google"""
    try:
        session = extract_session_from_url()
        if session:
            # Mettre à jour la session Supabase
            conn.auth.set_session(session)
            st.success("✅ Connexion réussie !")
            st.rerun()
    except Exception as e:
        st.error(f"❌ Erreur lors de l'authentification : {str(e)}")

def sign_in_with_google():
    """Initialise la connexion avec Google"""
    try:
        # Configurer l'authentification Google
        auth_config = {
            "provider": "google",
            "options": {
                "redirectTo": "https://notemaster-v2-jkvg9zktfpwttpjuxzwcpe.streamlit.app/auth",
                "queryParams": {
                    "access_type": "offline",
                    "prompt": "consent",
                }
            }
        }
        
        # Générer l'URL d'authentification
        auth_response = conn.auth.sign_in_with_oauth(auth_config)
        
        # Vérifier si nous avons une URL
        if hasattr(auth_response, 'url'):
            auth_url = auth_response.url
            
            # Utiliser JavaScript pour ouvrir dans un nouvel onglet
            js = f'''window.open("{auth_url}", "_blank");'''
            st.components.v1.html(
                f'''
                <script>{js}</script>
                <div style="padding: 10px; border: 1px solid #f0f2f6; border-radius: 5px; background-color: #f8f9fa;">
                    <p>⚠️ Une nouvelle fenêtre va s'ouvrir pour l'authentification Google.</p>
                    <p>Une fois connecté, revenez sur cette fenêtre et <strong>rafraîchissez la page</strong>.</p>
                </div>
                ''',
                height=150
            )
            
            return auth_url
        else:
            st.error("❌ Impossible d'obtenir l'URL d'authentification")
            return None
        
    except Exception as e:
        st.error("❌ Erreur lors de l'authentification")
        st.error(f"Message : {str(e)}")
        return None

def sign_out():
    """Déconnexion de l'utilisateur"""
    return conn.auth.sign_out()
