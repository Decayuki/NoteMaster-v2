import streamlit as st
import sys
import os
import json
import requests
from datetime import datetime

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.supabase import get_user_session
from src.utils.database import (
    get_user_subjects, get_user_chapters, get_user_notes, 
    get_user_quiz_questions, save_quiz_question, save_quiz_response
)
from src.config import VERSION

def generate_questions_from_notes(notes_content, num_questions=3):
    """Génère des questions à partir du contenu des notes en utilisant l'API OpenAI"""
    try:
        # Vérifier si la clé API est disponible
        if 'OPENAI_API_KEY' not in st.secrets:
            st.error("❌ Clé API OpenAI non configurée.")
            return None
        
        api_key = st.secrets['OPENAI_API_KEY']
        
        # Préparer le prompt pour l'API
        system_prompt = (
            "Tu es un assistant pédagogique spécialisé dans la création de questions d'examen. "
            "Génère exactement {} questions pertinentes basées sur le contenu des notes fournies. "
            "Pour chaque question, fournis également une réponse modèle détaillée. "
            "Format exact de la réponse (en JSON) : "
            "[{{"
            "\"question\": \"La question posée\", "
            "\"answer\": \"La réponse modèle détaillée\""
            "}}]"
        ).format(num_questions)
        
        user_prompt = f"Voici le contenu des notes : {notes_content}"
        
        # Importer OpenAI
        import openai
        
        # Configurer l'API OpenAI
        openai.api_key = api_key
        
        # Appel à l'API OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Traiter la réponse de l'API OpenAI
        content = response.choices[0].message.content
        
        # Extraire le JSON de la réponse
        try:
            # Tenter de parser directement
            questions = json.loads(content)
            return questions
        except json.JSONDecodeError:
            # Si échec, essayer d'extraire le JSON de la réponse textuelle
            try:
                # Chercher le début et la fin du JSON
                start = content.find('[{')
                end = content.rfind('}]') + 2
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    questions = json.loads(json_str)
                    return questions
            except:
                st.error("❌ Impossible de parser la réponse JSON.")
                st.code(content)
                return None
    
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération des questions: {str(e)}")
        return None

def show_quiz_page():
    """Affiche la page de quiz"""
    
    # Vérifier si l'utilisateur est connecté
    user = get_user_session()
    if not user:
        st.warning("Vous devez être connecté pour accéder à vos quiz.")
        if st.button("Se connecter"):
            st.switch_page("src/pages/login.py")
        return
    
    st.title("Quiz - NoteMaster v{}".format(VERSION))
    st.write("Testez vos connaissances sur les sujets que vous avez étudiés.")
    
    # Récupérer les matières de l'utilisateur
    subjects = get_user_subjects()
    
    if not subjects:
        st.error("Erreur lors de la récupération des matières.")
        return
    
    # Créer une liste de noms de matières pour le selectbox
    subject_names = [subject["name"] for subject in subjects]
    subject_ids = {subject["name"]: subject["id"] for subject in subjects}
    
    # Sélection de la matière
    selected_subject_name = st.selectbox("📚 Sélectionnez une matière", subject_names, key="quiz_subject")
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
        selected_chapter_name = st.selectbox("📑 Sélectionnez un chapitre", chapter_names, key="quiz_chapter")
        selected_chapter_id = chapter_ids.get(selected_chapter_name)
        
        if selected_chapter_id:
            st.markdown(f"## Quiz - {selected_subject_name} - {selected_chapter_name}")
            
            # Récupérer les notes de l'utilisateur pour ce chapitre
            notes = get_user_notes(chapter_id=selected_chapter_id)
            
            if not notes:
                st.info("ℹ️ Aucune note disponible pour ce chapitre. Commencez par prendre des notes !")
                if st.button("Aller à la page des notes"):
                    st.switch_page("src/pages/notes.py")
                return
            
            # Récupérer les questions existantes pour ce chapitre
            existing_questions = get_user_quiz_questions(selected_chapter_id)
            
            # Afficher les questions existantes ou générer de nouvelles questions
            if existing_questions:
                st.success(f"✅ {len(existing_questions)} questions disponibles pour ce chapitre.")
                
                # Bouton pour générer de nouvelles questions
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🎯 Générer de nouvelles questions"):
                        st.session_state.generate_new_questions = True
                with col2:
                    if st.button("📝 Utiliser les questions existantes"):
                        st.session_state.show_existing_questions = True
                
                # Afficher les questions existantes
                if "show_existing_questions" in st.session_state and st.session_state.show_existing_questions:
                    show_quiz_questions(existing_questions, selected_chapter_id, selected_subject_id)
            
            # Générer de nouvelles questions
            if "generate_new_questions" not in st.session_state:
                st.session_state.generate_new_questions = len(existing_questions) == 0
            
            if st.session_state.generate_new_questions:
                with st.spinner("Génération des questions en cours..."):
                    # Combiner le contenu de toutes les notes
                    notes_content = "\n\n".join([f"# {note['title']}\n{note['content']}" for note in notes])
                    
                    # Générer des questions à partir des notes
                    questions = generate_questions_from_notes(notes_content)
                    
                    if questions:
                        # Sauvegarder les questions dans Supabase
                        for q in questions:
                            save_quiz_question(
                                question=q["question"],
                                answer=q["answer"],
                                chapter_id=selected_chapter_id,
                                subject_id=selected_subject_id
                            )
                        
                        st.success(f"✅ {len(questions)} nouvelles questions générées avec succès !")
                        
                        # Afficher les questions générées
                        show_quiz_questions(questions, selected_chapter_id, selected_subject_id)
                        
                        # Réinitialiser l'état
                        st.session_state.generate_new_questions = False
                    else:
                        st.error("❌ Impossible de générer des questions. Veuillez réessayer.")

def show_quiz_questions(questions, chapter_id, subject_id):
    """Affiche les questions de quiz et permet à l'utilisateur d'y répondre"""
    
    for i, question in enumerate(questions):
        q_text = question.get("question", question.get("question", ""))
        a_text = question.get("answer", question.get("answer", ""))
        
        with st.expander(f"Question {i+1}: {q_text[:50]}...", expanded=i==0):
            st.markdown(f"**{q_text}**")
            
            # Zone de réponse
            user_answer = st.text_area(f"Votre réponse à la question {i+1}", key=f"answer_{i}")
            
            # Bouton pour vérifier la réponse
            if st.button("Vérifier ma réponse", key=f"check_{i}"):
                if user_answer:
                    # Sauvegarder la réponse
                    question_id = question.get("id", f"temp_{i}")
                    save_quiz_response(
                        question_id=question_id,
                        user_response=user_answer,
                        score=0  # Le score sera mis à jour plus tard
                    )
                    
                    # Afficher la réponse modèle
                    st.markdown("### Réponse modèle:")
                    st.markdown(a_text)
                    
                    # Auto-évaluation
                    st.markdown("### Auto-évaluation:")
                    score = st.slider("Notez votre réponse de 0 à 5", 0, 5, 3, key=f"score_{i}")
                    
                    if st.button("Enregistrer mon score", key=f"save_score_{i}"):
                        # Mettre à jour le score
                        save_quiz_response(
                            question_id=question_id,
                            user_response=user_answer,
                            score=score
                        )
                        st.success("✅ Score enregistré !")
                else:
                    st.warning("⚠️ Veuillez rédiger une réponse avant de la vérifier.")
