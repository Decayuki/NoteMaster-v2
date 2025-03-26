import streamlit as st
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.supabase import conn

def show_notes_page():
    """Affiche la page de prise de notes"""
    
    # Sélection de la matière
    subjects = ["Science de gestion"]  # Pour l'instant en dur, à récupérer de Supabase plus tard
    selected_subject = st.selectbox("📚 Sélectionnez une matière", subjects)
    
    if selected_subject:
        # Sélection du chapitre
        chapters = [f"Chapitre {i}" for i in range(1, 11)]  # À récupérer de Supabase
        selected_chapter = st.selectbox("📑 Sélectionnez un chapitre", chapters)
        
        if selected_chapter:
            st.markdown(f"## {selected_subject} - {selected_chapter}")
            
            # Zone de titre de la note
            note_title = st.text_input("Titre de la note")
            
            # Zone de contenu de la note
            note_content = st.text_area("Contenu de la note", height=300)
            
            # Bouton de sauvegarde
            if st.button("💾 Sauvegarder la note"):
                if note_title and note_content:
                    try:
                        # Sauvegarder dans Supabase
                        note = {
                            "user_id": st.session_state.user.id,
                            "subject": selected_subject,
                            "chapter": selected_chapter,
                            "title": note_title,
                            "content": note_content
                        }
                        conn.table("notes").insert(note).execute()
                        st.success("Note sauvegardée avec succès !")
                        
                        # Vider les champs
                        st.text_input("Titre de la note", value="")
                        st.text_area("Contenu de la note", value="", height=300)
                    except Exception as e:
                        st.error(f"Erreur lors de la sauvegarde : {str(e)}")
                else:
                    st.warning("Veuillez remplir le titre et le contenu de la note.")
