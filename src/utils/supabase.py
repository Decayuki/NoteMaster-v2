import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialiser la connexion Supabase
conn = st.connection('supabase', type=SupabaseConnection)
supabase = conn.client

def get_user_session():
    """Récupère la session utilisateur actuelle"""
    try:
        return conn.auth.get_user()
    except Exception:
        return None

def sign_in_with_google():
    """Initialise la connexion avec Google"""
    try:
        # Configurer l'authentification Google
        auth_config = {
            "provider": "google",
            "options": {
                "redirectTo": "https://notemaster-v2-jkvg9zktfpwttpjuxzwcpe.streamlit.app",
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
