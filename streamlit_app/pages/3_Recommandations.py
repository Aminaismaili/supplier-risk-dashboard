import streamlit as st
import sys
sys.path.append('.')
from streamlit_app.utils.api_client import api_client
import pandas as pd

st.set_page_config(page_title="Recommandations", page_icon="", layout="wide")

st.title(" Recommandations & Plan d'Action")
st.markdown("### Actions intelligentes générées par IA")

st.markdown("---")

st.sidebar.header(" Sélection Fournisseur")

supplier_selector = st.sidebar.selectbox(
    "Choisir un profil type",
    ["Fournisseur à Risque Élevé", "Fournisseur à Risque Moyen", "Fournisseur à Risque Faible"]
)

if supplier_selector == "Fournisseur à Risque Élevé":
    supplier_data = {
        "country": "Chine",
        "region": "APAC",
        "sector": "automotive",
        "family": "Électronique",
        "years_in_business": 5,
        "revenue_millions": 10.0,
        "profit_margin": 2.0,
        "debt_ratio": 0.85,
        "liquidity_ratio": 0.8,
        "financial_health_score": 3.0,
        "on_time_delivery_rate": 70.0,
        "quality_defect_rate": 5.0,
        "lead_time_days": 60,
        "capacity_utilization": 95.0,
        "geopolitical_risk": 8.0,
        "supply_chain_disruption_history": 5,
        "cybersecurity_incidents": 2,
        "labor_disputes": 3,
        "environmental_score": 4.0
    }
elif supplier_selector == "Fournisseur à Risque Moyen":
    supplier_data = {
        "country": "Turquie",
        "region": "EMEA",
        "sector": "automotive",
        "family": "Injection",
        "years_in_business": 12,
        "revenue_millions": 30.0,
        "profit_margin": 6.0,
        "debt_ratio": 0.55,
        "liquidity_ratio": 1.4,
        "financial_health_score": 6.0,
        "on_time_delivery_rate": 85.0,
        "quality_defect_rate": 2.5,
        "lead_time_days": 35,
        "capacity_utilization": 80.0,
        "geopolitical_risk": 5.0,
        "supply_chain_disruption_history": 2,
        "cybersecurity_incidents": 1,
        "labor_disputes": 1,
        "environmental_score": 6.5
    }
else:
    supplier_data = {
        "country": "Allemagne",
        "region": "EMEA",
        "sector": "aeronautic",
        "family": "Composite",
        "years_in_business": 25,
        "revenue_millions": 100.0,
        "profit_margin": 12.0,
        "debt_ratio": 0.25,
        "liquidity_ratio": 2.2,
        "financial_health_score": 9.0,
        "on_time_delivery_rate": 98.0,
        "quality_defect_rate": 0.5,
        "lead_time_days": 15,
        "capacity_utilization": 75.0,
        "geopolitical_risk": 2.0,
        "supply_chain_disruption_history": 0,
        "cybersecurity_incidents": 0,
        "labor_disputes": 0,
        "environmental_score": 8.5
    }

if st.sidebar.button(" Analyser & Générer Recommandations", type="primary", use_container_width=True):
    with st.spinner(" Génération des recommandations IA..."):
        result = api_client.predict_supplier(supplier_data)
        
        if result:
            st.success(" Analyse terminée et recommandations générées")
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            risk_level = result['predicted_risk_level'].upper()
            
            with col1:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                        <h3 style='margin: 0;'>Niveau de Risque</h3>
                        <h2 style='margin: 0.5rem 0 0 0; font-size: 2rem;'>{risk_level}</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                        <h3 style='margin: 0;'>Score de Risque</h3>
                        <h2 style='margin: 0.5rem 0 0 0; font-size: 2rem;'>{result['risk_score']:.2f}/10</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                        <h3 style='margin: 0;'>Actions à Mener</h3>
                        <h2 style='margin: 0.5rem 0 0 0; font-size: 2rem;'>{len(result['recommendations'])}</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.subheader(" Plan d'Action Recommandé")
            
            recommendations = result['recommendations']
            
            priority_order = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
            recommendations_sorted = sorted(
                recommendations, 
                key=lambda x: priority_order.get(x['priority'], 4)
            )
            
            for idx, rec in enumerate(recommendations_sorted, 1):
                priority = rec['priority']
                
                if priority == 'HIGH':
                    color = '#e74c3c'
                    icon = '🔴'
                elif priority == 'MEDIUM':
                    color = '#f39c12'
                    icon = '🟡'
                else:
                    color = '#2ecc71'
                    icon = '🟢'
                
                with st.expander(f"{icon} **Action #{idx} - Priorité {priority}**", expanded=(idx <= 2)):
                    st.markdown(f"""
                        <div style='padding: 1rem; background: #f8f9fa; border-left: 5px solid {color}; border-radius: 5px;'>
                            <h4 style='color: {color}; margin-top: 0;'>📌 {rec['action']}</h4>
                            <p><b>Impact Estimé:</b> {rec['impact']}</p>
                            <p><b>Priorité:</b> {priority}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_action1, col_action2 = st.columns(2)
                    
                    with col_action1:
                        if st.button(f" Marquer comme complétée", key=f"complete_{idx}"):
                            st.success(f"Action #{idx} marquée comme complétée !")
                    
                    with col_action2:
                        if st.button(f" Planifier", key=f"schedule_{idx}"):
                            st.info(f"Planification de l'action #{idx}")
            
            st.markdown("---")
            
            st.subheader(" Résumé des Recommandations")
            
            df_recommendations = pd.DataFrame(recommendations)
            
            st.dataframe(
                df_recommendations[['priority', 'action', 'impact']],
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            
            st.subheader(" Exporter le Plan d'Action")
            
            col_exp1, col_exp2, col_exp3 = st.columns(3)
            
            with col_exp1:
                csv = df_recommendations.to_csv(index=False)
                st.download_button(
                    " Export CSV",
                    csv,
                    f"action_plan_{result['supplier_id']}.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col_exp2:
                import json
                json_data = json.dumps(recommendations, indent=2)
                st.download_button(
                    " Export JSON",
                    json_data,
                    f"action_plan_{result['supplier_id']}.json",
                    "application/json",
                    use_container_width=True
                )
            
            with col_exp3:
                if st.button(" Envoyer par Email", use_container_width=True):
                    st.info(" Fonctionnalité d'envoi d'email à implémenter")
        
        else:
            st.error(" Erreur lors de la génération des recommandations")

else:
    st.info(" Sélectionnez un profil de fournisseur et cliquez sur 'Analyser'")
    
    st.markdown("""
        <div style='background: #f8f9fa; padding: 2rem; border-radius: 10px;'>
            <h3 style='color: #1f77b4;'> À propos des Recommandations</h3>
            <p>Le système génère automatiquement un plan d'action personnalisé basé sur:</p>
            <ul>
                <li> Le niveau de risque global du fournisseur</li>
                <li> Les catégories de risque identifiées</li>
                <li> Les meilleures pratiques de l'industrie</li>
                <li> L'historique des actions efficaces</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
