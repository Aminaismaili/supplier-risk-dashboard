import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_risk_gauge(risk_score: float, risk_level: str):
    color_map = {
        'low': 'green',
        'medium': 'orange',
        'high': 'red',
        'critical': 'darkred'
    }
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Risk Score", 'font': {'size': 24}},
        delta={'reference': 5},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color_map.get(risk_level, 'gray')},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 3], 'color': 'lightgreen'},
                {'range': [3, 5], 'color': 'lightyellow'},
                {'range': [5, 7], 'color': 'orange'},
                {'range': [7, 10], 'color': 'lightcoral'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def create_probability_chart(probabilities: dict):
    df = pd.DataFrame({
        'Risk Level': list(probabilities.keys()),
        'Probability': [v * 100 for v in probabilities.values()]
    })
    
    color_map = {
        'low': '#2ecc71',
        'medium': '#f39c12',
        'high': '#e74c3c',
        'critical': '#c0392b'
    }
    
    fig = px.bar(
        df,
        x='Risk Level',
        y='Probability',
        color='Risk Level',
        color_discrete_map=color_map,
        text='Probability'
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        showlegend=False,
        height=400,
        yaxis_title="Probability (%)",
        xaxis_title="Risk Level"
    )
    
    return fig

def create_radar_chart(risk_details: list):
    df = pd.DataFrame(risk_details)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=df['score'],
        theta=df['category'],
        fill='toself',
        fillcolor='rgba(31, 119, 180, 0.5)',
        line=dict(color='rgb(31, 119, 180)', width=2),
        name='Risk Scores'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        height=400
    )
    
    return fig

def create_distribution_pie(risk_distribution: dict):
    df = pd.DataFrame({
        'Risk Level': list(risk_distribution.keys()),
        'Count': list(risk_distribution.values())
    })
    
    color_map = {
        'low': '#2ecc71',
        'medium': '#f39c12',
        'high': '#e74c3c',
        'critical': '#c0392b'
    }
    
    fig = px.pie(
        df,
        values='Count',
        names='Risk Level',
        color='Risk Level',
        color_discrete_map=color_map,
        hole=0.4
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig