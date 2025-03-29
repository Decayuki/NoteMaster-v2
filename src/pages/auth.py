import streamlit as st
from src.utils.supabase import handle_auth_callback

# Configuration de la page
st.set_page_config(
    page_title="NoteMaster - Authentification",
    page_icon="🔐",
    initial_sidebar_state="collapsed"
)

# Masquer le menu Streamlit
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

# Vérifier si un code d'autorisation est présent dans l'URL
code = st.query_params.get("code", None)

if code:
    # Si un code est présent, gère l'authentification
    if handle_auth_callback(code):
        st.success("✅ Authentification réussie!")
        st.markdown("""
        <div style="text-align: center">
            <p>Vous êtes maintenant connecté. Vous allez être redirigé vers le tableau de bord...</p>
            <a href="/" target="_self">
                <button style="
                    background-color: #4285F4;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                ">
                    Aller au tableau de bord
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Erreur lors de l'authentification")
        st.markdown("""
        <div style="text-align: center">
            <p>Une erreur s'est produite lors de l'authentification. Veuillez réessayer.</p>
            <a href="/" target="_self">
                <button style="
                    background-color: #4285F4;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: bold;
                ">
                    Retour à l'accueil
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
else:
    # Si aucun code n'est présent, afficher un message et rediriger vers l'accueil
    st.info("🔄 Aucun code d'authentification détecté. Redirection vers la page d'accueil...")
    st.markdown("""
    <div style="text-align: center">
        <a href="/" target="_self">
            <button style="
                background-color: #4285F4;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            ">
                Retour à l'accueil
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
