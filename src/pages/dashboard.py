import streamlit as st

def show_dashboard():
    """Affiche le tableau de bord de l'utilisateur"""
    st.title("Tableau de bord NoteMaster")
    
    # Afficher les options principales
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
