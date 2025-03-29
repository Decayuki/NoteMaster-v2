import streamlit as st
import json

# Configuration de la page
st.set_page_config(
    page_title="NoteMaster - Page de débogage",
    page_icon="🔐",
    initial_sidebar_state="expanded"
)

st.title("Page de débogage d'authentification")

# Afficher tous les paramètres d'URL pour le débogage
st.subheader("Paramètres d'URL actuels")
all_params = st.query_params.to_dict()
st.json(all_params)

# Vérifier si un code d'autorisation est présent dans l'URL
code = st.query_params.get("code", None)

if code:
    st.success("Un code d'authentification a été trouvé dans l'URL!")
    st.code(code, language="text")
    
    # Afficher des instructions pour tester manuellement
    st.subheader("Instructions pour continuer")
    st.write("""
    1. Copiez ce code d'authentification
    2. Retournez à la page d'accueil
    3. Ajoutez manuellement le paramètre ?code=VOTRE_CODE à l'URL de la page d'accueil
    4. Appuyez sur Entrée pour soumettre l'URL
    """)
    
    # Bouton pour retourner à l'accueil
    st.markdown(f"""
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
else:
    st.warning("Aucun code d'authentification n'a été trouvé dans l'URL.")
    st.info("""
    Pour tester l'authentification:
    1. Retournez à la page d'accueil
    2. Cliquez sur "Se connecter avec Google"
    3. Après l'authentification Google, vous serez redirigé ici avec un code dans l'URL
    """)
    
    # Bouton pour retourner à l'accueil
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
