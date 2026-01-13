Architecture du Système
=======================

Vue Globale
-----------

Le système est structuré autour d’un pipeline modulaire couvrant tout le cycle de vie
des données et des modèles :

1. Génération des données
2. Préprocessing & Feature Engineering
3. Modélisation & Tracking MLOps
4. Exposition via API REST
5. Visualisation et monitoring

Pipeline Fonctionnel
--------------------

- **Données** : données fournisseurs synthétiques versionnées avec DVC
- **ML** : modèles de prédiction entraînés et suivis avec MLflow
- **API** : FastAPI pour l’inférence en temps réel
- **Dashboard** : Streamlit pour la visualisation des KPIs
