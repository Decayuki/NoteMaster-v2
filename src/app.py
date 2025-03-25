import streamlit as st
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

# Importer et exécuter la page d'accueil
from Home import main

if __name__ == "__main__":
    main()
