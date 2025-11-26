from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from api.models.schemas import (
    SupplierInput,
    PredictionResponse,
    HealthResponse,
    StatsResponse,
    RiskDetail,
    Recommendation
)
from api.services.ml_service import get_ml_service, MLService
from api.config import settings
import pandas as pd

logger = logging.getLogger(__name__)
router = APIRouter()

def get_ml_service_dependency() -> MLService:
    return get_ml_service(
        settings.MODEL_PATH,
        settings.LABEL_ENCODER_PATH,
        settings.LABEL_ENCODERS_PATH
    )

@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check"
)
async def health_check(ml_service: MLService = Depends(get_ml_service_dependency)):
    return HealthResponse(
        status="healthy",
        api_version=settings.API_VERSION,
        model_loaded=ml_service.is_loaded()
    )

@router.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Predictions"],
    summary="Predict supplier risk"
)
async def predict_risk(
    supplier: SupplierInput,
    ml_service: MLService = Depends(get_ml_service_dependency)
):
    try:
        supplier_dict = supplier.dict()
        
        prediction = ml_service.predict(supplier_dict)
        
        risk_details = [RiskDetail(**detail) for detail in prediction['risk_details']]
        recommendations = [Recommendation(**rec) for rec in prediction['recommendations']]
        
        return PredictionResponse(
            supplier_id=f"SUP_{hash(str(supplier_dict)) % 10000:04d}",
            predicted_risk_level=prediction['predicted_risk_level'],
            risk_probability=prediction['risk_probability'],
            confidence=prediction['confidence'],
            risk_score=prediction['risk_score'],
            risk_details=risk_details,
            recommendations=recommendations,
            model_version=ml_service.get_model_version()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get(
    "/stats",
    response_model=StatsResponse,
    tags=["Statistics"],
    summary="Get dataset statistics"
)
async def get_statistics():
    try:
        df = pd.read_csv('data/processed/suppliers_processed.csv')
        
        return StatsResponse(
            total_suppliers=len(df),
            risk_distribution=df['risk_level'].value_counts().to_dict(),
            sectors={}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))