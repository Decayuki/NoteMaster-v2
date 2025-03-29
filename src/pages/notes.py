import streamlit as st
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.supabase import get_user_session
from src.utils.database import get_user_subjects, get_user_chapters, get_user_notes, save_note

def show_notes_page():
    """Affiche la page de prise de notes"""
    
    # Vérifier si l'utilisateur est connecté
    user = get_user_session()
    if not user:
        st.warning("Vous devez être connecté pour accéder à vos notes.")
        if st.button("Se connecter"):
            st.switch_page("src/pages/login.py")
        return
    
    # Récupérer les matières de l'utilisateur
    subjects = get_user_subjects()
    
    if not subjects:
        st.error("Erreur lors de la récupération des matières.")
        return
    
    # Créer une liste de noms de matières pour le selectbox
    subject_names = [subject["name"] for subject in subjects]
    subject_ids = {subject["name"]: subject["id"] for subject in subjects}
    
    # Sélection de la matière
    selected_subject_name = st.selectbox("📚 Sélectionnez une matière", subject_names)
    selected_subject_id = subject_ids.get(selected_subject_name)
    
    if selected_subject_id:
        # Récupérer les chapitres de la matière
        chapters = get_user_chapters(selected_subject_id)
        
        if not chapters:
            st.error("Erreur lors de la récupération des chapitres.")
            return
        
        # Créer une liste de noms de chapitres pour le selectbox
        chapter_names = [chapter["name"] for chapter in chapters]
        chapter_ids = {chapter["name"]: chapter["id"] for chapter in chapters}
        
        # Sélection du chapitre
        selected_chapter_name = st.selectbox("📑 Sélectionnez un chapitre", chapter_names)
        selected_chapter_id = chapter_ids.get(selected_chapter_name)
        
        if selected_chapter_id:
            st.markdown(f"## {selected_subject_name} - {selected_chapter_name}")
            
            # Afficher les notes existantes pour ce chapitre
            existing_notes = get_user_notes(chapter_id=selected_chapter_id)
            
            if existing_notes:
                with st.expander("📝 Notes existantes", expanded=False):
                    for note in existing_notes:
                        st.markdown(f"### {note['title']}")
                        st.markdown(note['content'])
                        st.markdown("---")
            
            # Zone de titre de la note
            note_title = st.text_input("Titre de la note")
            
            # Zone de contenu de la note
            note_content = st.text_area("Contenu de la note", height=300)
            
            # Bouton de sauvegarde
            if st.button("💾 Sauvegarder la note"):
                if note_title and note_content:
                    # Sauvegarder dans Supabase
                    success = save_note(
                        title=note_title,
                        content=note_content,
                        chapter_id=selected_chapter_id,
                        subject_id=selected_subject_id
                    )
                    
                    if success:
                        st.success("✅ Note sauvegardée avec succès !")
                        # Réinitialiser les champs
                        st.text_input("Titre de la note", value="")
                        st.text_area("Contenu de la note", value="", height=300)
                        # Recharger la page pour afficher la nouvelle note
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la sauvegarde de la note.")
                else:
                    st.warning("⚠️ Veuillez remplir le titre et le contenu de la note.")
