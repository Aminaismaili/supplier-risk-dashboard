#!/bin/bash

echo " Démarrage du Supplier Risk Dashboard..."
echo "=========================================="

# Démarrer l'API FastAPI en arrière-plan
echo " Démarrage de l'API FastAPI..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Attendre que l'API démarre
sleep 3

# Démarrer Streamlit
echo " Démarrage du Dashboard Streamlit..."
streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0

# Cleanup : arrêter l'API quand Streamlit s'arrête
kill $API_PID
