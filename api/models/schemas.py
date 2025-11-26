from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class SupplierInput(BaseModel):
    country: str = "Maroc"
    region: str = "EMEA"
    sector: str = "automotive"
    family: str = "Câblage"
    years_in_business: int = 15
    revenue_millions: float = 25.5
    profit_margin: float = 8.5
    debt_ratio: float = 0.45
    liquidity_ratio: float = 1.8
    financial_health_score: float = 7.2
    on_time_delivery_rate: float = 92.5
    quality_defect_rate: float = 1.5
    lead_time_days: int = 25
    capacity_utilization: float = 78.5
    geopolitical_risk: float = 3.5
    supply_chain_disruption_history: int = 1
    cybersecurity_incidents: int = 0
    labor_disputes: int = 0
    environmental_score: float = 7.8

class RiskDetail(BaseModel):
    category: str
    score: float
    level: str

class Recommendation(BaseModel):
    priority: str
    action: str
    impact: str

class PredictionResponse(BaseModel):
    supplier_id: str
    predicted_risk_level: str
    risk_probability: Dict[str, float]
    confidence: float
    risk_score: float
    risk_details: List[RiskDetail]
    recommendations: List[Recommendation]
    timestamp: datetime = Field(default_factory=datetime.now)
    model_version: str

class HealthResponse(BaseModel):
    status: str
    api_version: str
    model_loaded: bool
    timestamp: datetime = Field(default_factory=datetime.now)

class StatsResponse(BaseModel):
    total_suppliers: int
    risk_distribution: Dict[str, int]
    sectors: Dict[str, int]