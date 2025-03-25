import streamlit as st
import sys
import os

# Ajouter le répertoire src au PYTHONPATH
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(src_path)

try:
    from src.app import main
    main()
except Exception as e:
    st.error("### ❌ Erreur lors du chargement de l'application")
    st.error(f"Message : {str(e)}")
    
    st.write("### 🔍 Informations de débogage")
    st.json({
        "PYTHONPATH": sys.path,
        "src_path": src_path,
        "current_dir": os.getcwd(),
        "files_in_src": os.listdir(src_path) if os.path.exists(src_path) else "src n'existe pas",
        "files_in_root": os.listdir(os.path.dirname(os.path.abspath(__file__)))
    })
