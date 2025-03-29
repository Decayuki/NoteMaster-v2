import streamlit as st
from src.utils.supabase import conn, get_user_session, get_user_info

def get_user_subjects(user_id=None):
    """
    Récupère les matières de l'utilisateur.
    Si aucune matière n'existe, crée une matière par défaut.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return []
        user_id = user.user.id
    
    try:
        # Récupérer les matières de l'utilisateur
        response = conn.table("subjects")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        
        subjects = response.data
        
        # Si aucune matière n'existe, créer une matière par défaut
        if not subjects:
            default_subject = {
                "user_id": user_id,
                "name": "Science de gestion",
                "description": "Cours de science de gestion"
            }
            
            result = conn.table("subjects").insert(default_subject).execute()
            subjects = result.data
        
        return subjects
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des matières : {str(e)}")
        return []

def get_user_chapters(subject_id, user_id=None):
    """
    Récupère les chapitres d'une matière pour l'utilisateur.
    Si aucun chapitre n'existe, crée des chapitres par défaut.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return []
        user_id = user.user.id
    
    try:
        # Récupérer les chapitres de la matière
        response = conn.table("chapters")\
            .select("*")\
            .eq("subject_id", subject_id)\
            .eq("user_id", user_id)\
            .execute()
        
        chapters = response.data
        
        # Si aucun chapitre n'existe, créer des chapitres par défaut
        if not chapters:
            default_chapters = []
            for i in range(1, 6):  # Créer 5 chapitres par défaut
                default_chapters.append({
                    "user_id": user_id,
                    "subject_id": subject_id,
                    "name": f"Chapitre {i}",
                    "description": f"Chapitre {i} de la matière"
                })
            
            result = conn.table("chapters").insert(default_chapters).execute()
            chapters = result.data
        
        return chapters
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des chapitres : {str(e)}")
        return []

def get_user_notes(chapter_id=None, subject_id=None, user_id=None):
    """
    Récupère les notes de l'utilisateur pour un chapitre spécifique.
    Si chapter_id est None, récupère toutes les notes de l'utilisateur.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return []
        user_id = user.user.id
    
    try:
        # Construire la requête de base
        query = conn.table("notes").select("*").eq("user_id", user_id)
        
        # Filtrer par chapitre si spécifié
        if chapter_id:
            query = query.eq("chapter_id", chapter_id)
        
        # Filtrer par matière si spécifié
        if subject_id:
            query = query.eq("subject_id", subject_id)
        
        # Exécuter la requête
        response = query.execute()
        
        return response.data
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des notes : {str(e)}")
        return []

def save_note(title, content, chapter_id, subject_id, user_id=None):
    """
    Sauvegarde une note pour l'utilisateur.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return False
        user_id = user.user.id
    
    try:
        # Créer la note
        note = {
            "user_id": user_id,
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "title": title,
            "content": content
        }
        
        # Sauvegarder dans Supabase
        conn.table("notes").insert(note).execute()
        
        return True
    
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde de la note : {str(e)}")
        return False

def get_user_quiz_questions(chapter_id, user_id=None):
    """
    Récupère les questions de quiz pour un chapitre spécifique.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return []
        user_id = user.user.id
    
    try:
        # Récupérer les questions de quiz
        response = conn.table("quiz_questions")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("chapter_id", chapter_id)\
            .execute()
        
        return response.data
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des questions : {str(e)}")
        return []

def save_quiz_question(question, answer, chapter_id, subject_id, user_id=None):
    """
    Sauvegarde une question de quiz pour l'utilisateur.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return False
        user_id = user.user.id
    
    try:
        # Créer la question
        quiz_question = {
            "user_id": user_id,
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "question": question,
            "answer": answer
        }
        
        # Sauvegarder dans Supabase
        conn.table("quiz_questions").insert(quiz_question).execute()
        
        return True
    
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde de la question : {str(e)}")
        return False

def save_quiz_response(question_id, user_response, score, user_id=None):
    """
    Sauvegarde la réponse d'un utilisateur à une question de quiz.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return False
        user_id = user.user.id
    
    try:
        # Créer la réponse
        response_data = {
            "user_id": user_id,
            "question_id": question_id,
            "response": user_response,
            "score": score
        }
        
        # Sauvegarder dans Supabase
        conn.table("quiz_responses").insert(response_data).execute()
        
        return True
    
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde de la réponse : {str(e)}")
        return False

def get_user_progress(user_id=None):
    """
    Récupère les statistiques de progression de l'utilisateur.
    """
    if not user_id:
        user = get_user_session()
        if not user:
            return None
        user_id = user.user.id
    
    try:
        # Récupérer le nombre de notes
        notes_count = len(get_user_notes(user_id=user_id))
        
        # Récupérer les réponses aux quiz
        quiz_responses = conn.table("quiz_responses")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        
        # Calculer le score moyen
        responses = quiz_responses.data
        total_score = sum(response.get("score", 0) for response in responses) if responses else 0
        avg_score = total_score / len(responses) if responses else 0
        
        return {
            "notes_count": notes_count,
            "quiz_responses_count": len(responses),
            "average_score": avg_score
        }
    
    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques : {str(e)}")
        return None
