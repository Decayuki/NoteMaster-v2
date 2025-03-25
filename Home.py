import streamlit as st
import sys
import os

# Configuration de base de Streamlit
st.set_page_config(
    page_title="NoteMaster",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style personnalisé
st.markdown("""
    <style>
        .stButton button {
            width: 100%;
            background-color: #4285F4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .main {
            background-color: #0E1117;
        }
        .st-emotion-cache-18ni7ap {
            background-color: #262730;
        }
        .stAlert {
            background-color: #262730;
            color: white;
        }
        .stExpander {
            background-color: #262730;
            border: 1px solid #4285F4;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Ajouter le répertoire src au PYTHONPATH
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(src_path)

try:
    from src.pages.login import show_login_page
    from src.pages.notes import show_notes_page
    from src.pages.quiz import show_quiz_page
    from src.utils.supabase import get_user_session
    
    # Vérifier la session utilisateur
    session = get_user_session()
    
    if not session:
        show_login_page()
    else:
        # Stocker les informations utilisateur dans la session
        st.session_state.user = session.user
        
        # Sidebar avec navigation
        with st.sidebar:
            st.title(f"NoteMaster v2.0.0")
            st.write(f"👤 {st.session_state.user.email}")
            
            # Menu de navigation
            selected = st.radio(
                "Navigation",
                ["📝 Mes Notes", "❓ Quiz", "📊 Statistiques"],
                index=0
            )
        
        # Afficher la page sélectionnée
        if selected == "📝 Mes Notes":
            show_notes_page()
        elif selected == "❓ Quiz":
            show_quiz_page()
        else:
            st.title("📊 Mes Statistiques")
            # TODO: Implémenter les statistiques
            
except Exception as e:
    st.error("### ❌ Erreur lors du chargement de l'application")
    st.error(f"Message : {str(e)}")
    st.error("Stack trace :")
    import traceback
    st.code(traceback.format_exc())
    
    st.write("### 🔍 Informations de débogage")
    st.json({
        "PYTHONPATH": sys.path,
        "src_path": src_path,
        "current_dir": os.getcwd(),
        "files_in_src": os.listdir(src_path) if os.path.exists(src_path) else "src n'existe pas",
        "files_in_root": os.listdir(os.path.dirname(os.path.abspath(__file__)))
    })
