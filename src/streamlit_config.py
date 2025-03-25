import streamlit as st

def configure_streamlit():
    """Configure l'apparence et le comportement de Streamlit"""
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
