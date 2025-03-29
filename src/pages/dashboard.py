import streamlit as st
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.supabase import get_user_session, get_user_info
from src.utils.database import get_user_subjects, get_user_progress
from src.config import VERSION

def show_dashboard():
    """Affiche le tableau de bord de l'utilisateur"""
    # Vérifier si l'utilisateur est connecté
    user_session = get_user_session()
    if not user_session:
        st.warning("Vous devez être connecté pour accéder à votre tableau de bord.")
        if st.button("Se connecter"):
            st.switch_page("src/pages/login.py")
        return
    
    # Récupérer les informations de l'utilisateur
    user_info = get_user_info()
    
    # En-tête avec informations utilisateur
    st.title(f"Tableau de bord NoteMaster v{VERSION}")
    
    # Afficher les informations de l'utilisateur
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if user_info and user_info.get("avatar_url"):
            st.image(user_info["avatar_url"], width=100)
        else:
            st.markdown("### 👤")
    
    with col2:
        if user_info:
            st.markdown(f"### Bienvenue, {user_info.get('name', user_info.get('email', 'Utilisateur'))} !")
            st.markdown(f"*Connecté avec {user_info.get('email', '')}*")
        else:
            st.markdown("### Bienvenue !")
    
    # Récupérer les statistiques de progression
    progress = get_user_progress()
    
    # Afficher les statistiques
    st.markdown("## Votre progression")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("📝 Notes créées", progress.get("notes_count", 0) if progress else 0)
    
    with stat_col2:
        st.metric("🎯 Quiz complétés", progress.get("quiz_responses_count", 0) if progress else 0)
    
    with stat_col3:
        avg_score = progress.get("average_score", 0) if progress else 0
        st.metric("🏆 Score moyen", f"{avg_score:.1f}/5")
    
    # Récupérer les matières de l'utilisateur
    subjects = get_user_subjects()
    if subjects:
        st.markdown("## Vos matières")
        for subject in subjects:
            st.markdown(f"- {subject['name']}")
    
    # Afficher les options principales
    st.markdown("## Accéder à vos ressources")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📝 **Notes**", icon="📝")
        st.write("Gérez vos notes de cours et vos résumés")
        if st.button("Accéder aux notes", key="notes_btn"):
            st.switch_page("src/pages/notes.py")
            
    with col2:
        st.info("🎯 **Quiz**", icon="🎯")
        st.write("Testez vos connaissances avec des quiz")
        if st.button("Accéder aux quiz", key="quiz_btn"):
            st.switch_page("src/pages/quiz.py")
    
    # Afficher un bouton de déconnexion
    st.markdown("---")
    if st.button("🚪 Se déconnecter"):
        from src.utils.supabase import sign_out
        sign_out()
        st.rerun()
