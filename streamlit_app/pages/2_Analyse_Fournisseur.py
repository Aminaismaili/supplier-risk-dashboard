import streamlit as st
import sys
sys.path.append('.')
from streamlit_app.utils.api_client import api_client
from streamlit_app.utils.charts import create_risk_gauge, create_probability_chart, create_radar_chart

st.set_page_config(page_title="Analyse Fournisseur", page_icon="", layout="wide")

st.title(" Analyse Fournisseur - Prédiction Détaillée")
st.markdown("### Configuration des paramètres fournisseur pour prédiction IA")

st.markdown("---")

with st.sidebar:
    st.header(" Configuration Fournisseur")
    
    with st.expander(" Informations Générales", expanded=True):
        country = st.selectbox("Pays", ["Maroc", "France", "Allemagne", "Chine", "Thaïlande", "Espagne", "Turquie", "Pologne", "Mexique", "États-Unis"])
        region = st.selectbox("Région", ["EMEA", "APAC", "NA", "LATAM"])
        sector = st.selectbox("Secteur", ["automotive", "aeronautic"])
        family = st.selectbox("Famille", ["Câblage", "Injection", "Filtration", "Composite", "Usinage", "Électronique"])
    
    with st.expander(" Métriques Financières", expanded=True):
        years_in_business = st.slider("Années d'activité", 1, 50, 15)
        revenue_millions = st.number_input("Chiffre d'affaires (M€)", 1.0, 1000.0, 25.5, 0.1)
        profit_margin = st.slider("Marge bénéficiaire (%)", -10.0, 30.0, 8.5, 0.5)
        debt_ratio = st.slider("Ratio d'endettement", 0.0, 1.0, 0.45, 0.01)
        liquidity_ratio = st.slider("Ratio de liquidité", 0.0, 3.0, 1.8, 0.1)
        financial_health_score = st.slider("Score santé financière", 0.0, 10.0, 7.2, 0.1)
    
    with st.expander(" Métriques Opérationnelles", expanded=True):
        on_time_delivery_rate = st.slider("Taux livraison à temps (%)", 0.0, 100.0, 92.5, 0.5)
        quality_defect_rate = st.slider("Taux de défauts qualité (%)", 0.0, 10.0, 1.5, 0.1)
        lead_time_days = st.slider("Délai de livraison (jours)", 1, 90, 25)
        capacity_utilization = st.slider("Utilisation capacité (%)", 0.0, 100.0, 78.5, 0.5)
    
    with st.expander(" Facteurs de Risque", expanded=True):
        geopolitical_risk = st.slider("Risque géopolitique", 0.0, 10.0, 3.5, 0.1)
        supply_chain_disruption_history = st.slider("Historique perturbations", 0, 10, 1)
        cybersecurity_incidents = st.slider("Incidents cybersécurité", 0, 5, 0)
        labor_disputes = st.slider("Conflits sociaux", 0, 5, 0)
        environmental_score = st.slider("Score environnemental", 0.0, 10.0, 7.8, 0.1)
    
    st.markdown("---")
    predict_button = st.button(" Lancer la Prédiction", type="primary", use_container_width=True)

if predict_button:
    supplier_data = {
        "country": country,
        "region": region,
        "sector": sector,
        "family": family,
        "years_in_business": years_in_business,
        "revenue_millions": revenue_millions,
        "profit_margin": profit_margin,
        "debt_ratio": debt_ratio,
        "liquidity_ratio": liquidity_ratio,
        "financial_health_score": financial_health_score,
        "on_time_delivery_rate": on_time_delivery_rate,
        "quality_defect_rate": quality_defect_rate,
        "lead_time_days": lead_time_days,
        "capacity_utilization": capacity_utilization,
        "geopolitical_risk": geopolitical_risk,
        "supply_chain_disruption_history": supply_chain_disruption_history,
        "cybersecurity_incidents": cybersecurity_incidents,
        "labor_disputes": labor_disputes,
        "environmental_score": environmental_score
    }
    
    with st.spinner(" Analyse en cours par le modèle IA..."):
        result = api_client.predict_supplier(supplier_data)
        
        if result:
            st.success(" Prédiction réussie !")
            
            st.markdown("---")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            risk_level = result['predicted_risk_level'].upper()
            risk_colors = {
                'LOW': '🟢',
                'MEDIUM': '🟡',
                'HIGH': '🔴',
                'CRITICAL': '��'
            }
            
            with col1:
                st.metric("Niveau de Risque", f"{risk_colors.get(risk_level, '⚪')} {risk_level}")
            
            with col2:
                st.metric("Score de Risque", f"{result['risk_score']:.2f}/10")
            
            with col3:
                st.metric("Confiance Modèle", f"{result['confidence']*100:.1f}%")
            
            with col4:
                st.metric("ID Fournisseur", result['supplier_id'])
            
            with col5:
                st.metric("Version Modèle", result['model_version'])
            
            st.markdown("---")
            
            col_left, col_middle, col_right = st.columns(3)
            
            with col_left:
                st.subheader(" Score de Risque Global")
                fig_gauge = create_risk_gauge(result['risk_score'], result['predicted_risk_level'])
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col_middle:
                st.subheader(" Distribution des Probabilités")
                fig_prob = create_probability_chart(result['risk_probability'])
                st.plotly_chart(fig_prob, use_container_width=True)
            
            with col_right:
                st.subheader(" Analyse Multi-dimensionnelle")
                fig_radar = create_radar_chart(result['risk_details'])
                st.plotly_chart(fig_radar, use_container_width=True)
            
            st.markdown("---")
            
            st.subheader(" Détail des Risques par Catégorie")
            
            import pandas as pd
            df_details = pd.DataFrame(result['risk_details'])
            
            def highlight_risk(row):
                if row['level'] == 'HIGH':
                    return ['background-color: #ffcccc'] * len(row)
                elif row['level'] == 'MEDIUM':
                    return ['background-color: #ffffcc'] * len(row)
                else:
                    return ['background-color: #ccffcc'] * len(row)
            
            st.dataframe(
                df_details.style.apply(highlight_risk, axis=1).format({'score': '{:.2f}'}),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            
            st.subheader(" Exporter les Résultats")
            
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                csv = df_details.to_csv(index=False)
                st.download_button(
                    label=" Télécharger CSV",
                    data=csv,
                    file_name=f"risk_analysis_{result['supplier_id']}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_export2:
                import json
                json_data = json.dumps(result, indent=2)
                st.download_button(
                    label=" Télécharger JSON",
                    data=json_data,
                    file_name=f"risk_analysis_{result['supplier_id']}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        else:
            st.error(" Erreur lors de la prédiction. Vérifiez que l'API est démarrée.")

else:
    st.info(" Configurez les paramètres dans la barre latérale et cliquez sur 'Lancer la Prédiction'")
    
    st.markdown("""
        <div style='background: #f8f9fa; padding: 2rem; border-radius: 10px; border-left: 5px solid #1f77b4;'>
            <h3 style='color: #1f77b4;'> Guide d'Utilisation</h3>
            <ol>
                <li><b>Renseignez les informations générales</b> du fournisseur (pays, secteur, famille)</li>
                <li><b>Ajustez les métriques financières</b> selon les données disponibles</li>
                <li><b>Définissez les métriques opérationnelles</b> (livraison, qualité, capacité)</li>
                <li><b>Évaluez les facteurs de risque</b> externes (géopolitique, incidents)</li>
                <li><b>Lancez la prédiction</b> pour obtenir l'analyse IA complète</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
