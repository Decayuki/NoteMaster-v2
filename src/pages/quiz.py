import streamlit as st
import sys
import os

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.supabase import supabase

def show_quiz_page():
    """Affiche la page de quiz"""
    
    # Sélection de la matière
    subjects = ["Science de gestion"]  # À récupérer de Supabase
    selected_subject = st.selectbox("📚 Sélectionnez une matière", subjects, key="quiz_subject")
    
    if selected_subject:
        # Sélection du chapitre
        chapters = [f"Chapitre {i}" for i in range(1, 11)]  # À récupérer de Supabase
        selected_chapter = st.selectbox("📑 Sélectionnez un chapitre", chapters, key="quiz_chapter")
        
        if selected_chapter:
            # Récupérer les notes de l'utilisateur pour ce chapitre
            try:
                notes = supabase.table("notes")\
                    .select("*")\
                    .eq("user_id", st.session_state.user.id)\
                    .eq("subject", selected_subject)\
                    .eq("chapter", selected_chapter)\
                    .execute()
                
                if notes.data:
                    st.markdown(f"## Quiz - {selected_subject} - {selected_chapter}")
                    
                    # Bouton pour générer des questions
                    if st.button("🎯 Générer des questions"):
                        with st.spinner("Génération des questions en cours..."):
                            # TODO: Implémenter la génération de questions avec OpenAI
                            st.info("Fonctionnalité en cours de développement...")
                else:
                    st.info("Aucune note disponible pour ce chapitre. Commencez par prendre des notes !")
            except Exception as e:
                st.error(f"Erreur lors de la récupération des notes : {str(e)}")
