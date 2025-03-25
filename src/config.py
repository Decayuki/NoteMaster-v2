import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configuration OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuration de l'application
APP_NAME = "NoteMaster"
VERSION = "0.8.0"

# URLs de l'application
APP_URLS = {
    "local": {
        "base": "http://localhost:8501",
        "redirect": "http://localhost:8501/*",
        "callback": "https://rygktzcbjsigbfkodobx.supabase.co/auth/v1/callback"
    },
    "cloud": {
        "base": "https://notemaster-v2-jkvg9zktfpwttpjuxzwcpe.streamlit.app",
        "redirect": "https://notemaster-v2-jkvg9zktfpwttpjuxzwcpe.streamlit.app/*",
        "callback": "https://rygktzcbjsigbfkodobx.supabase.co/auth/v1/callback"
    }
}

# Configuration de l'authentification
def get_redirect_url():
    """Retourne l'URL de redirection en fonction de l'environnement"""
    env = "cloud" if os.getenv("IS_STREAMLIT_CLOUD") == "true" else "local"
    return APP_URLS[env]["base"]

def get_auth_redirect_url():
    """Retourne l'URL de redirection pour l'authentification"""
    env = "cloud" if os.getenv("IS_STREAMLIT_CLOUD") == "true" else "local"
    return APP_URLS[env]["redirect"]

def get_auth_callback_url():
    """Retourne l'URL de callback pour l'authentification"""
    return APP_URLS["cloud"]["callback"]
