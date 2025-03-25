from supabase import create_client
from ..config import SUPABASE_URL, SUPABASE_KEY

# Créer le client Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_session():
    """Récupère la session utilisateur actuelle"""
    return supabase.auth.get_session()

def sign_in_with_google():
    """Initialise la connexion avec Google"""
    return supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": "http://localhost:8501"  # URL de redirection après connexion
        }
    })

def sign_out():
    """Déconnexion de l'utilisateur"""
    return supabase.auth.sign_out()
