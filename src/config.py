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
VERSION = "2.0.0"

# Configuration de l'authentification
def get_redirect_url():
    # Vérifier si nous sommes sur Streamlit Cloud
    if os.getenv("IS_STREAMLIT_CLOUD") == "true":
        return "https://notemaster-v2-jkvg9zktfpwttpjuxzwcpe.streamlit.app"
    return "http://localhost:8501"
