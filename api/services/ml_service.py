import joblib
import pandas as pd
import numpy as np
from typing import Dict, List
from pathlib import Path
import logging
import sys

sys.path.append('src')
from features.feature_engineering import FeatureEngineer

logger = logging.getLogger(__name__)

class MLService:
    
    def __init__(self, model_path: str, label_encoder_path: str, label_encoders_path: str):
        self.model_path = Path(model_path)
        self.label_encoder_path = Path(label_encoder_path)
        self.label_encoders_path = Path(label_encoders_path)
        
        self.model = None
        self.label_encoder = None
        self.feature_engineer = None
        
        self._load_model()
    
    def _load_model(self):
        try:
            self.model = joblib.load(self.model_path)
            logger.info(f"Model loaded from {self.model_path}")
            
            self.label_encoder = joblib.load(self.label_encoder_path)
            logger.info(f"Label encoder loaded from {self.label_encoder_path}")
            
            self.feature_engineer = FeatureEngineer()
            label_encoders = joblib.load(self.label_encoders_path)
            self.feature_engineer.label_encoders = label_encoders
            logger.info(f"Feature engineer loaded")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def is_loaded(self) -> bool:
        return self.model is not None and self.label_encoder is not None
    
    def get_model_version(self) -> str:
        return "v1.0"
    
    def predict(self, supplier_data: Dict) -> Dict:
        if not self.is_loaded():
            raise ValueError("Model not loaded")
        
        try:
            input_data = self._prepare_input(supplier_data)
            df = pd.DataFrame([input_data])
            
            df = self.feature_engineer.create_features(df)
            df = self.feature_engineer.encode_categorical(df)
            X, _ = self.feature_engineer.prepare_for_ml(df)
            
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            
            risk_level = self.label_encoder.inverse_transform([prediction])[0]
            
            risk_probs = {
                label: float(prob) 
                for label, prob in zip(self.label_encoder.classes_, probabilities)
            }
            
            confidence = float(probabilities[prediction])
            risk_score = float(max(probabilities) * 10)
            
            risk_details = self._calculate_risk_details(supplier_data)
            recommendations = self._generate_recommendations(risk_level, supplier_data)
            
            return {
                'predicted_risk_level': risk_level,
                'risk_probability': risk_probs,
                'confidence': confidence,
                'risk_score': risk_score,
                'risk_details': risk_details,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
    
    def _prepare_input(self, supplier_data: Dict) -> Dict:
        return {
            'country': supplier_data.get('country', 'Maroc'),
            'region': supplier_data.get('region', 'EMEA'),
            'sector': supplier_data.get('sector', 'automotive'),
            'family': supplier_data.get('family', 'Câblage'),
            'single_source': 'no',
            'distance_km': 500.0,
            'years_in_business': supplier_data.get('years_in_business', 15),
            'certification_iso': 'yes',
            'revenue_millions': supplier_data.get('revenue_millions', 25.5),
            'profit_margin': supplier_data.get('profit_margin', 8.5),
            'debt_ratio': supplier_data.get('debt_ratio', 0.45),
            'liquidity_ratio': supplier_data.get('liquidity_ratio', 1.8),
            'payment_delay_days': 5,
            'financial_health_score': supplier_data.get('financial_health_score', 7.2),
            'otd_3m': supplier_data.get('on_time_delivery_rate', 92.5),
            'avg_delay_days_3m': 2.0,
            'delay_volatility_3m': 1.0,
            'otd_6m': supplier_data.get('on_time_delivery_rate', 92.5),
            'avg_delay_days_6m': 2.0,
            'on_time_delivery_rate': supplier_data.get('on_time_delivery_rate', 92.5),
            'lead_time_days': supplier_data.get('lead_time_days', 25),
            'ppm_3m': 100,
            'defect_rate_3m': supplier_data.get('quality_defect_rate', 1.5),
            'quality_defect_rate': supplier_data.get('quality_defect_rate', 1.5),
            'cpk_latest': 1.3,
            'recurring_8d': 0,
            'capacity_utilization': supplier_data.get('capacity_utilization', 78.5),
            'cert_iatf16949': 'yes',
            'iatf_16949': 'yes' if supplier_data.get('sector') == 'automotive' else 'no',
            'cert_as9100': 'yes',
            'as9100': 'yes' if supplier_data.get('sector') == 'aeronautic' else 'no',
            'cert_expiry_next90d': 'no',
            'reach_compliance': 'yes',
            'esg_score': 75.0,
            'environmental_score': supplier_data.get('environmental_score', 7.8),
            'non_conformity_flag': 'no',
            'country_risk_index': int(supplier_data.get('geopolitical_risk', 3.5) * 10),
            'geopolitical_risk': supplier_data.get('geopolitical_risk', 3.5),
            'trade_barrier_flag': 'no',
            'route_disruption_flag': 'no',
            'supply_chain_disruption_history': supplier_data.get('supply_chain_disruption_history', 1),
            'cybersecurity_incidents': supplier_data.get('cybersecurity_incidents', 0),
            'labor_disputes': supplier_data.get('labor_disputes', 0),
        }
    
    def _calculate_risk_details(self, supplier_data: Dict) -> List[Dict]:
        financial_risk = (supplier_data.get('debt_ratio', 0.5) * 100)
        operational_risk = (100 - supplier_data.get('on_time_delivery_rate', 90))
        quality_risk = (supplier_data.get('quality_defect_rate', 2) * 20)
        geopolitical_risk = (supplier_data.get('geopolitical_risk', 3) * 10)
        compliance_risk = (10 - supplier_data.get('environmental_score', 7)) * 10
        
        return [
            {
                'category': 'Financial Risk',
                'score': round(financial_risk, 2),
                'level': self._get_level(financial_risk)
            },
            {
                'category': 'Operational Risk',
                'score': round(operational_risk, 2),
                'level': self._get_level(operational_risk)
            },
            {
                'category': 'Quality Risk',
                'score': round(quality_risk, 2),
                'level': self._get_level(quality_risk)
            },
            {
                'category': 'Geopolitical Risk',
                'score': round(geopolitical_risk, 2),
                'level': self._get_level(geopolitical_risk)
            },
            {
                'category': 'Compliance Risk',
                'score': round(compliance_risk, 2),
                'level': self._get_level(compliance_risk)
            }
        ]
    
    def _get_level(self, score: float) -> str:
        if score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_recommendations(self, risk_level: str, supplier_data: Dict) -> List[Dict]:
        recommendations = []
        
        if risk_level in ["high", "critical"]:
            recommendations.extend([
                {
                    'priority': 'HIGH',
                    'action': 'Immediate audit required',
                    'impact': 'Critical - Reduce risk by 30%'
                },
                {
                    'priority': 'HIGH',
                    'action': 'Activate backup suppliers',
                    'impact': 'High - Ensure supply continuity'
                },
                {
                    'priority': 'MEDIUM',
                    'action': 'Renegotiate delivery terms',
                    'impact': 'Medium - Improve delivery rate by 15%'
                }
            ])
        elif risk_level == "medium":
            recommendations.extend([
                {
                    'priority': 'MEDIUM',
                    'action': 'Quarterly performance review',
                    'impact': 'Medium - Monitor trends'
                },
                {
                    'priority': 'MEDIUM',
                    'action': 'Request certification updates',
                    'impact': 'Low - Maintain compliance'
                }
            ])
        else:
            recommendations.extend([
                {
                    'priority': 'LOW',
                    'action': 'Maintain standard monitoring',
                    'impact': 'Low - Continue good performance'
                },
                {
                    'priority': 'LOW',
                    'action': 'Annual partnership review',
                    'impact': 'Low - Strengthen relationship'
                }
            ])
        
        return recommendations

_ml_service_instance = None

def get_ml_service(model_path: str, label_encoder_path: str, label_encoders_path: str) -> MLService:
    global _ml_service_instance
    
    if _ml_service_instance is None:
        _ml_service_instance = MLService(model_path, label_encoder_path, label_encoders_path)
    
    return _ml_service_instance