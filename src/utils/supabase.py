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
        # Vérifier si un code d'autorisation est présent dans l'URL
        code = st.query_params.get("code", None)
        
        if code:
            try:
                # Essayer d'échanger le code contre une session
                session = conn.auth.exchange_code_for_session({'auth_code': code})
                if session:
                    st.success("✅ Connexion réussie !")
                    # Effacer les paramètres d'URL pour éviter les problèmes de rafraîchissement
                    st.query_params.clear()
                    # Recharger la page pour appliquer la session
                    st.rerun()
                    return True
            except Exception as e:
                st.error(f"❌ Erreur lors de l'échange du code : {str(e)}")
            return False
        
        # Configurer l'authentification Google
        auth_config = {
            "provider": "google",
            "options": {
                "redirectTo": "https://rygktzcbjsigbfkodobx.supabase.co/auth/v1/callback",
                "scopes": "email profile",
                "queryParams": {
                    "access_type": "offline",
                    "prompt": "consent",
                    "redirect_uri": "https://rygktzcbjsigbfkodobx.supabase.co/auth/v1/callback"
                }
            }
        }
        
        try:
            # Générer l'URL d'authentification
            auth_url = conn.auth.sign_in_with_oauth(auth_config)
            
            # Utiliser JavaScript pour ouvrir dans un nouvel onglet
            js = f'''window.open("{auth_url['url']}", "_blank");'''
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
            
            return auth_url["url"]
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
    return conn.auth.sign_out()
