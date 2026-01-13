import requests
import pandas as pd
from typing import Dict, List, Optional

API_URL = "http://localhost:8000"

class APIClient:
    
    def __init__(self):
        self.base_url = API_URL
    
    def check_health(self) -> Dict:
        try:
            response = requests.get(f"{self.base_url}/api/v1/health", timeout=2)
            return response.json() if response.status_code == 200 else {"status": "error"}
        except:
            return {"status": "offline"}
    
    def predict_supplier(self, supplier_data: Dict) -> Optional[Dict]:
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/predict",
                json=supplier_data,
                timeout=10
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    def get_stats(self) -> Optional[Dict]:
        try:
            response = requests.get(f"{self.base_url}/api/v1/stats", timeout=5)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def batch_predict(self, suppliers_data: List[Dict]) -> List[Dict]:
        results = []
        for supplier in suppliers_data:
            result = self.predict_supplier(supplier)
            if result:
                results.append(result)
        return results

# Instance globale
api_client = APIClient()