import streamlit as st
from st_supabase_connection import SupabaseConnection
import secrets
import hashlib
import base64

# Initialiser la connexion Supabase
conn = st.connection('supabase', type=SupabaseConnection)
supabase = conn.client

def generate_pkce_pair():
    """Génère une paire code_verifier/code_challenge pour PKCE"""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge

def get_user_session():
    """Récupère la session utilisateur actuelle"""
    try:
        return conn.auth.get_user()
    except Exception:
        return None

def sign_in_with_google():
    """Initialise la connexion avec Google"""
    try:
        # Vérifier si un code d'autorisation est présent dans l'URL
        code = st.query_params.get("code", None)
        
        if code:
            try:
                # Récupérer le code_verifier de la session
                code_verifier = st.session_state.get('code_verifier')
                if not code_verifier:
                    st.error("❌ Code verifier manquant. Veuillez réessayer la connexion.")
                    return False
                
                # Essayer d'échanger le code contre une session
                session = conn.auth.exchange_code_for_session({
                    'auth_code': code,
                    'code_verifier': code_verifier
                })
                
                if session:
                    st.success("✅ Connexion réussie !")
                    # Nettoyer la session
                    if 'code_verifier' in st.session_state:
                        del st.session_state['code_verifier']
                    # Effacer les paramètres d'URL
                    st.query_params.clear()
                    # Recharger la page
                    st.rerun()
                    return True
            except Exception as e:
                st.error(f"❌ Erreur lors de l'échange du code : {str(e)}")
            return False
        
        # Générer une paire PKCE
        code_verifier, code_challenge = generate_pkce_pair()
        # Sauvegarder le code_verifier pour plus tard
        st.session_state['code_verifier'] = code_verifier
        
        # Configurer l'authentification Google
        auth_config = {
            "provider": "google",
            "options": {
                "redirectTo": "https://rygktzcbjsigbfkodobx.supabase.co/auth/v1/callback",
                "scopes": "email profile",
                "queryParams": {
                    "access_type": "offline",
                    "prompt": "consent",
                    "code_challenge": code_challenge,
                    "code_challenge_method": "S256",
                    "redirect_uri": "https://rygktzcbjsigbfkodobx.supabase.co/auth/v1/callback"
                }
            }
        }
        
        try:
            # Générer l'URL d'authentification
            auth_response = conn.auth.sign_in_with_oauth(auth_config)
            
            # Vérifier si nous avons une URL
            if hasattr(auth_response, 'url'):
                auth_url = auth_response.url
            else:
                st.error("❌ Impossible d'obtenir l'URL d'authentification")
                return None
            
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
        except Exception as e:
            st.error("❌ Erreur lors de l'authentification")
            st.error(f"Message : {str(e)}")
            return None
            
    except Exception as e:
        st.error("❌ Erreur lors de l'authentification")
        st.error(f"Message : {str(e)}")
        return None

def sign_out():
    """Déconnexion de l'utilisateur"""
    # Nettoyer la session
    if 'code_verifier' in st.session_state:
        del st.session_state['code_verifier']
    return conn.auth.sign_out()
