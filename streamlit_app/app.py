import streamlit as st
import sys
sys.path.append('.')
from streamlit_app.utils.api_client import api_client
from streamlit_app.utils.styling import apply_custom_styling
from streamlit_app.utils.charts import create_distribution_pie
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Global", page_icon="", layout="wide")

# Cacher la sidebar Streamlit
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

apply_custom_styling()

st.markdown('<h1 class="big-title">Dashboard Global</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Vue d\'ensemble des risques fournisseurs en temps réel</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

try:
    stats = api_client.get_stats()
    
    if stats:
        total = stats.get('total_suppliers', 0)
        risk_dist = stats.get('risk_distribution', {})
        
        low_count = risk_dist.get('low', 0)
        medium_count = risk_dist.get('medium', 0)
        high_count = risk_dist.get('high', 0)
        critical_count = risk_dist.get('critical', 0)
        
        # Vérifier le statut de l'API
        try:
            health = api_client.check_health()
            api_status = "Online"
            api_color = "#10b981"
            api_icon = "🟢"
        except:
            api_status = "Offline"
            api_color = "#ef4444"
            api_icon = "🔴"
        
        # KPI Cards avec design moderne + API Status
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">LOW RISK</div>
                    <div class="metric-value" style="color: #10b981;">{low_count}</div>
                    <div class="metric-delta positive">{low_count/total*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">MEDIUM RISK</div>
                    <div class="metric-value" style="color: #f59e0b;">{medium_count}</div>
                    <div class="metric-delta">{medium_count/total*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">HIGH RISK</div>
                    <div class="metric-value" style="color: #ef4444;">{high_count}</div>
                    <div class="metric-delta negative">{high_count/total*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">CRITICAL</div>
                    <div class="metric-value" style="color: #8b5cf6;">{critical_count}</div>
                    <div class="metric-delta negative">{critical_count/total*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">API STATUS</div>
                    <div class="metric-value" style="color: {api_color};">{api_icon} {api_status}</div>
                    <div class="metric-delta neutral">Real-time</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Section graphiques
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("""
                <div class="chart-container">
                    <h3 style='margin-top: 0; color: #1f2937;'>Distribution des Risques</h3>
                </div>
            """, unsafe_allow_html=True)
            
            fig_pie = create_distribution_pie(risk_dist)
            fig_pie.update_layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                height=400,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_right:
            st.markdown("""
                <div class="chart-container">
                    <h3 style='margin-top: 0; color: #1f2937;'>Analyse par Niveau</h3>
                </div>
            """, unsafe_allow_html=True)
            
            df_risk = pd.DataFrame({
                'Risk Level': ['Low', 'Medium', 'High', 'Critical'],
                'Count': [low_count, medium_count, high_count, critical_count],
                'Percentage': [
                    low_count/total*100,
                    medium_count/total*100,
                    high_count/total*100,
                    critical_count/total*100
                ]
            })
            
            fig_bar = px.bar(
                df_risk,
                x='Risk Level',
                y='Count',
                color='Risk Level',
                color_discrete_map={
                    'Low': '#10b981',
                    'Medium': '#f59e0b',
                    'High': '#ef4444',
                    'Critical': '#8b5cf6'
                },
                text='Count'
            )
            fig_bar.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                marker_line_color='white',
                marker_line_width=2
            )
            fig_bar.update_layout(
                showlegend=False,
                height=400,
                paper_bgcolor='white',
                plot_bgcolor='white',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#f3f4f6'),
                margin=dict(t=50, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Statistiques détaillées
        st.markdown("""
            <div class="chart-container">
                <h3 style='margin-top: 0; color: #1f2937;'>Statistiques Détaillées</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.markdown(f"""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #6366f115 0%, #8b5cf615 100%); 
                            border-radius: 10px; border-left: 4px solid #6366f1;'>
                    <div style='font-size: 0.875rem; color: #6b7280; font-weight: 600; margin-bottom: 0.5rem;'>
                        TOTAL FOURNISSEURS
                    </div>
                    <div style='font-size: 2rem; font-weight: 700; color: #1f2937;'>
                        {total}
                    </div>
                    <div style='font-size: 0.875rem; color: #10b981; margin-top: 0.5rem;'>
                        Actifs
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            avg_risk = (high_count + critical_count) / total * 100 if total > 0 else 0
            st.markdown(f"""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #ef444415 0%, #dc262615 100%); 
                            border-radius: 10px; border-left: 4px solid #ef4444;'>
                    <div style='font-size: 0.875rem; color: #6b7280; font-weight: 600; margin-bottom: 0.5rem;'>
                        TAUX RISQUE ÉLEVÉ
                    </div>
                    <div style='font-size: 2rem; font-weight: 700; color: #1f2937;'>
                        {avg_risk:.1f}%
                    </div>
                    <div style='font-size: 0.875rem; color: #ef4444; margin-top: 0.5rem;'>
                        Attention requise
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat3:
            safe_ratio = low_count / total * 100 if total > 0 else 0
            st.markdown(f"""
                <div style='padding: 1.5rem; background: linear-gradient(135deg, #10b98115 0%, #059c6a15 100%); 
                            border-radius: 10px; border-left: 4px solid #10b981;'>
                    <div style='font-size: 0.875rem; color: #6b7280; font-weight: 600; margin-bottom: 0.5rem;'>
                        FOURNISSEURS SÛRS
                    </div>
                    <div style='font-size: 2rem; font-weight: 700; color: #1f2937;'>
                        {safe_ratio:.1f}%
                    </div>
                    <div style='font-size: 0.875rem; color: #10b981; margin-top: 0.5rem;'>
                        Performance optimale
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tableau récapitulatif 
        st.markdown("""
            <div class="chart-container">
                <h3 style='margin-top: 0; color: #1f2937;'>Tableau Récapitulatif</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Style le dataframe
        def style_dataframe(df):
            def highlight_row(row):
                if row['Risk Level'] == 'Critical':
                    return ['background-color: #8b5cf620'] * len(row)
                elif row['Risk Level'] == 'High':
                    return ['background-color: #ef444420'] * len(row)
                elif row['Risk Level'] == 'Medium':
                    return ['background-color: #f59e0b20'] * len(row)
                else:
                    return ['background-color: #10b98120'] * len(row)
            
            return df.style.apply(highlight_row, axis=1).format({
                'Percentage': '{:.2f}%'
            })
        
        st.dataframe(
            style_dataframe(df_risk),
            use_container_width=True,
            hide_index=True
        )
        
    else:
        st.warning("Impossible de récupérer les statistiques. Vérifiez que l'API est démarrée.")
        
except Exception as e:
    st.error(f"Erreur: {str(e)}")
    st.info("Vérifiez que l'API FastAPI est démarrée sur http://localhost:8000")

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 1rem; background: white; border-radius: 10px;'>
    </div>
""", unsafe_allow_html=True)
