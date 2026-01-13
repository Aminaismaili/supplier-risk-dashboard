import streamlit as st
import sys
sys.path.append('.')
from streamlit_app.utils.api_client import api_client
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Upload & Predict", page_icon="", layout="wide")

st.title(" Upload & Predict - Prédictions en Masse")
st.markdown("### Importez vos données et obtenez des prédictions pour plusieurs fournisseurs")

st.markdown("---")

tab1, tab2 = st.tabs([" Upload CSV", " Template"])

with tab2:
    st.markdown("###  Template CSV")
    
    st.markdown("""
        Téléchargez le template CSV ci-dessous et remplissez-le avec vos données :
        
        **Colonnes requises :**
        - country, region, sector, family
        - years_in_business, revenue_millions, profit_margin
        - debt_ratio, liquidity_ratio, financial_health_score
        - on_time_delivery_rate, quality_defect_rate
        - lead_time_days, capacity_utilization
        - geopolitical_risk, supply_chain_disruption_history
        - cybersecurity_incidents, labor_disputes, environmental_score
    """)
    
    template_data = {
        'country': ['Maroc', 'France'],
        'region': ['EMEA', 'EMEA'],
        'sector': ['automotive', 'aeronautic'],
        'family': ['Câblage', 'Composite'],
        'years_in_business': [15, 20],
        'revenue_millions': [25.5, 50.0],
        'profit_margin': [8.5, 12.0],
        'debt_ratio': [0.45, 0.30],
        'liquidity_ratio': [1.8, 2.1],
        'financial_health_score': [7.2, 8.5],
        'on_time_delivery_rate': [92.5, 96.0],
        'quality_defect_rate': [1.5, 0.8],
        'lead_time_days': [25, 18],
        'capacity_utilization': [78.5, 82.0],
        'geopolitical_risk': [3.5, 2.0],
        'supply_chain_disruption_history': [1, 0],
        'cybersecurity_incidents': [0, 0],
        'labor_disputes': [0, 0],
        'environmental_score': [7.8, 8.5]
    }
    
    template_df = pd.DataFrame(template_data)
    
    csv_template = template_df.to_csv(index=False)
    st.download_button(
        label=" Télécharger Template CSV",
        data=csv_template,
        file_name="template_suppliers.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("---")
    st.dataframe(template_df, use_container_width=True)

with tab1:
    st.markdown("###  Importer vos Données")
    
    uploaded_file = st.file_uploader(
        "Sélectionnez un fichier CSV",
        type=['csv'],
        help="Le fichier doit contenir les colonnes requises (voir Template)"
    )
    
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            
            st.success(f" Fichier chargé avec succès : {len(df_upload)} fournisseur(s)")
            
            st.markdown("###  Aperçu des Données")
            st.dataframe(df_upload.head(10), use_container_width=True)
            
            st.markdown("---")
            
            required_cols = [
                'country', 'region', 'sector', 'family',
                'years_in_business', 'revenue_millions', 'profit_margin',
                'debt_ratio', 'liquidity_ratio', 'financial_health_score',
                'on_time_delivery_rate', 'quality_defect_rate',
                'lead_time_days', 'capacity_utilization',
                'geopolitical_risk', 'supply_chain_disruption_history',
                'cybersecurity_incidents', 'labor_disputes', 'environmental_score'
            ]
            
            missing_cols = [col for col in required_cols if col not in df_upload.columns]
            
            if missing_cols:
                st.error(f" Colonnes manquantes : {', '.join(missing_cols)}")
                st.stop()
            
            st.success(" Toutes les colonnes requises sont présentes")
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                batch_size = st.number_input(
                    "Nombre de prédictions à effectuer",
                    min_value=1,
                    max_value=len(df_upload),
                    value=min(10, len(df_upload)),
                    help="Pour des raisons de performance, limitez à 50 max"
                )
            
            with col2:
                st.metric("Total Fournisseurs", len(df_upload))
            
            with col3:
                st.metric("Temps Estimé", f"{batch_size * 2}s")
            
            if st.button(" Lancer les Prédictions", type="primary", use_container_width=True):
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = []
                
                for idx, row in df_upload.head(batch_size).iterrows():
                    status_text.text(f"Analyse du fournisseur {idx + 1}/{batch_size}...")
                    progress_bar.progress((idx + 1) / batch_size)
                    
                    supplier_data = row.to_dict()
                    
                    result = api_client.predict_supplier(supplier_data)
                    
                    if result:
                        results.append({
                            'Index': idx + 1,
                            'Supplier ID': result['supplier_id'],
                            'Risk Level': result['predicted_risk_level'],
                            'Risk Score': result['risk_score'],
                            'Confidence': result['confidence'],
                            'Financial Risk': next((r['score'] for r in result['risk_details'] if r['category'] == 'Financial Risk'), 0),
                            'Operational Risk': next((r['score'] for r in result['risk_details'] if r['category'] == 'Operational Risk'), 0),
                            'Quality Risk': next((r['score'] for r in result['risk_details'] if r['category'] == 'Quality Risk'), 0),
                            'Actions Count': len(result['recommendations'])
                        })
                
                status_text.empty()
                progress_bar.empty()
                
                if results:
                    st.success(f" {len(results)} prédictions effectuées avec succès !")
                    
                    st.markdown("---")
                    
                    results_df = pd.DataFrame(results)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        critical_count = len(results_df[results_df['Risk Level'] == 'critical'])
                        st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #c0392b 0%, #8e44ad 100%); 
                                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                                <h3 style='margin: 0; font-size: 2rem;'>{critical_count}</h3>
                                <p style='margin: 0.5rem 0 0 0;'>Critical</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        high_count = len(results_df[results_df['Risk Level'] == 'high'])
                        st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                                <h3 style='margin: 0; font-size: 2rem;'>{high_count}</h3>
                                <p style='margin: 0.5rem 0 0 0;'>High Risk</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        medium_count = len(results_df[results_df['Risk Level'] == 'medium'])
                        st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); 
                                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                                <h3 style='margin: 0; font-size: 2rem;'>{medium_count}</h3>
                                <p style='margin: 0.5rem 0 0 0;'>Medium Risk</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        low_count = len(results_df[results_df['Risk Level'] == 'low'])
                        st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); 
                                        padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                                <h3 style='margin: 0; font-size: 2rem;'>{low_count}</h3>
                                <p style='margin: 0.5rem 0 0 0;'>Low Risk</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    st.markdown("###  Résultats des Prédictions")
                    
                    import plotly.express as px
                    
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        st.markdown("#### Distribution des Niveaux de Risque")
                        risk_counts = results_df['Risk Level'].value_counts()
                        fig_pie = px.pie(
                            values=risk_counts.values,
                            names=risk_counts.index,
                            color=risk_counts.index,
                            color_discrete_map={
                                'low': '#2ecc71',
                                'medium': '#f39c12',
                                'high': '#e74c3c',
                                'critical': '#8e44ad'
                            }
                        )
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col_chart2:
                        st.markdown("#### Scores de Risque")
                        fig_hist = px.histogram(
                            results_df,
                            x='Risk Score',
                            nbins=20,
                            color_discrete_sequence=['#1f77b4']
                        )
                        fig_hist.add_vline(x=5, line_dash="dash", line_color="orange")
                        fig_hist.add_vline(x=7, line_dash="dash", line_color="red")
                        st.plotly_chart(fig_hist, use_container_width=True)
                    
                    st.markdown("---")
                    
                    st.markdown("###  Tableau Détaillé des Résultats")
                    
                    def highlight_risk(row):
                        if row['Risk Level'] == 'critical':
                            return ['background-color: #8e44ad33'] * len(row)
                        elif row['Risk Level'] == 'high':
                            return ['background-color: #e74c3c33'] * len(row)
                        elif row['Risk Level'] == 'medium':
                            return ['background-color: #f39c1233'] * len(row)
                        else:
                            return ['background-color: #2ecc7133'] * len(row)
                    
                    st.dataframe(
                        results_df.style.apply(highlight_risk, axis=1).format({
                            'Risk Score': '{:.2f}',
                            'Confidence': '{:.2%}',
                            'Financial Risk': '{:.2f}',
                            'Operational Risk': '{:.2f}',
                            'Quality Risk': '{:.2f}'
                        }),
                        use_container_width=True,
                        height=400
                    )
                    
                    st.markdown("---")
                    
                    st.markdown("###  Exporter les Résultats")
                    
                    col_exp1, col_exp2, col_exp3 = st.columns(3)
                    
                    with col_exp1:
                        csv_results = results_df.to_csv(index=False)
                        st.download_button(
                            " Télécharger CSV Complet",
                            csv_results,
                            f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            "text/csv",
                            use_container_width=True
                        )
                    
                    with col_exp2:
                        high_risk_df = results_df[results_df['Risk Level'].isin(['high', 'critical'])]
                        if not high_risk_df.empty:
                            csv_high_risk = high_risk_df.to_csv(index=False)
                            st.download_button(
                                " Télécharger High Risk Only",
                                csv_high_risk,
                                f"high_risk_suppliers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                "text/csv",
                                use_container_width=True
                            )
                        else:
                            st.info("Aucun fournisseur à risque élevé")
                    
                    with col_exp3:
                        import json
                        json_results = json.dumps([r for r in results], indent=2)
                        st.download_button(
                            " Télécharger JSON",
                            json_results,
                            f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            "application/json",
                            use_container_width=True
                        )
                
                else:
                    st.error(" Aucune prédiction n'a pu être effectuée")
        
        except Exception as e:
            st.error(f" Erreur lors du traitement du fichier : {str(e)}")
    
    else:
        st.info(" Veuillez importer un fichier CSV pour commencer")
        
        st.markdown("""
            <div style='background: #f8f9fa; padding: 2rem; border-radius: 10px; margin-top: 2rem;'>
                <h3 style='color: #1f77b4;'> Instructions</h3>
                <ol>
                    <li>Téléchargez le template CSV depuis l'onglet "Template"</li>
                    <li>Remplissez-le avec vos données fournisseurs</li>
                    <li>Importez le fichier complété ci-dessus</li>
                    <li>Lancez les prédictions en masse</li>
                    <li>Exportez les résultats au format souhaité</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
