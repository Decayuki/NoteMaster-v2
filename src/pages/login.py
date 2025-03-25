import streamlit as st
from ..utils.supabase import sign_in_with_google, sign_out

def show_login_page():
    """Affiche la page de connexion"""
    st.title("Bienvenue sur NoteMaster")
    
    # Vérifier si l'utilisateur est déjà connecté
    if "user" in st.session_state:
        st.write(f"Connecté en tant que : {st.session_state.user.email}")
        if st.button("Se déconnecter"):
            sign_out()
            st.session_state.clear()
            st.rerun()
    else:
        st.write("Connectez-vous pour accéder à vos notes")
        
        # Bouton de connexion Google
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Se connecter avec Google", use_container_width=True):
                auth_url = sign_in_with_google()
                st.markdown(f'''
                    <a href="{auth_url}" target="_self">
                        <button style="
                            background-color: #4285F4;
                            color: white;
                            padding: 10px 20px;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            width: 100%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            gap: 10px;
                            font-family: Arial, sans-serif;
                        ">
                            <img src="https://www.google.com/favicon.ico" style="width: 20px; height: 20px;"/>
                            Continuer avec Google
                        </button>
                    </a>
                ''', unsafe_allow_html=True)
        
        # Message d'information
        st.info("""
        En vous connectant avec Google :
        - Accédez à vos notes depuis n'importe quel appareil
        - Gardez une trace de votre progression
        - Synchronisez automatiquement vos données
        """)
