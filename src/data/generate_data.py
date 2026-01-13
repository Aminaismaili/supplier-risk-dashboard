import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# Configuration
N = 1000
random.seed(42)
np.random.seed(42)

# Listes de valeurs possibles
countries = [
    "Maroc", "France", "Allemagne", "Chine", "Thaïlande", 
    "Espagne", "Turquie", "Pologne", "Mexique", "États-Unis"
]

regions = {
    "Maroc": "EMEA", "France": "EMEA", "Allemagne": "EMEA",
    "Chine": "APAC", "Thaïlande": "APAC", "Espagne": "EMEA",
    "Turquie": "EMEA", "Pologne": "EMEA", "Mexique": "LATAM",
    "États-Unis": "NA"
}

sectors = ["automotive", "aeronautic"]
families = ["Câblage", "Injection", "Filtration", "Composite", "Usinage", "Électronique"]
yes_no = ["yes", "no"]
criticity_levels = ["low", "medium", "high", "critical"]

def generate_supplier(i):
    country = random.choice(countries)
    sector = random.choice(sectors)
    
    # Distribution réaliste forcée: 50% low, 30% medium, 15% high, 5% critical
    random_dist = random.random()
    
    if random_dist < 0.05:
        target_risk = "critical"
        base_risk = random.uniform(7, 10)
    elif random_dist < 0.20:
        target_risk = "high"
        base_risk = random.uniform(5, 7)
    elif random_dist < 0.50:
        target_risk = "medium"
        base_risk = random.uniform(3, 5)
    else:
        target_risk = "low"
        base_risk = random.uniform(0.5, 3)
    
    # Générer des métriques cohérentes avec le niveau de risque
    if target_risk == "critical":
        otd = random.uniform(60, 75)
        ppm = int(np.random.lognormal(mean=8, sigma=0.5))
        debt_ratio = random.uniform(0.7, 0.95)
        country_risk = random.randint(70, 95)
        financial_health = random.uniform(0, 3)
        quality_defect = random.uniform(4, 10)
        incidents = random.randint(3, 7)
    elif target_risk == "high":
        otd = random.uniform(75, 85)
        ppm = int(np.random.lognormal(mean=7, sigma=0.5))
        debt_ratio = random.uniform(0.5, 0.8)
        country_risk = random.randint(50, 80)
        financial_health = random.uniform(3, 5)
        quality_defect = random.uniform(2, 5)
        incidents = random.randint(2, 4)
    elif target_risk == "medium":
        otd = random.uniform(85, 92)
        ppm = int(np.random.lognormal(mean=6, sigma=0.5))
        debt_ratio = random.uniform(0.3, 0.6)
        country_risk = random.randint(30, 60)
        financial_health = random.uniform(5, 7)
        quality_defect = random.uniform(1, 3)
        incidents = random.randint(1, 3)
    else:
        otd = random.uniform(92, 100)
        ppm = int(np.random.lognormal(mean=5, sigma=0.5))
        debt_ratio = random.uniform(0.1, 0.4)
        country_risk = random.randint(10, 40)
        financial_health = random.uniform(7, 10)
        quality_defect = random.uniform(0.1, 1.5)
        incidents = random.randint(0, 1)
    
    risk_score = base_risk
    
    return {
        "supplier_id": f"F{i:04d}",
        "supplier_name": f"Supplier_{i:04d}",
        "country": country,
        "region": regions[country],
        "sector": sector,
        "family": random.choice(families),
        "single_source": random.choice(yes_no),
        "distance_km": round(random.uniform(50, 1500), 1),
        
        "years_in_business": random.randint(1, 50),
        "certification_iso": random.choice(yes_no),
        
        "revenue_millions": round(np.random.lognormal(mean=3, sigma=1), 2),
        "profit_margin": round(random.uniform(-5, 20), 2),
        "debt_ratio": round(debt_ratio, 3),
        "liquidity_ratio": round(random.uniform(0.5, 2.5), 2),
        "payment_delay_days": random.randint(0, 30),
        "financial_health_score": round(financial_health, 2),
        
        "otd_3m": round(otd, 1),
        "avg_delay_days_3m": round(random.uniform(0, 6), 1),
        "delay_volatility_3m": round(random.uniform(0.3, 2.5), 2),
        
        "otd_6m": round(random.uniform(70, 100), 1),
        "avg_delay_days_6m": round(random.uniform(0, 6), 1),
        "on_time_delivery_rate": round(otd, 2),
        "lead_time_days": random.randint(5, 60),
        
        "ppm_3m": ppm,
        "defect_rate_3m": round(quality_defect, 2),
        "quality_defect_rate": round(quality_defect, 2),
        "cpk_latest": round(random.uniform(0.9, 1.6), 2),
        "recurring_8d": random.randint(0, 7),
        "capacity_utilization": round(random.uniform(50, 100), 2),
        
        "cert_iatf16949": random.choice(yes_no),
        "iatf_16949": random.choice(yes_no) if sector == "automotive" else "no",
        "cert_as9100": random.choice(yes_no),
        "as9100": random.choice(yes_no) if sector == "aeronautic" else "no",
        "cert_expiry_next90d": random.choice(yes_no),
        "reach_compliance": random.choice(["yes"] * 9 + ["no"]),
        "esg_score": round(random.uniform(40, 95), 1),
        "environmental_score": round(random.uniform(4, 9), 2),
        "non_conformity_flag": random.choice(yes_no),
        
        "country_risk_index": country_risk,
        "geopolitical_risk": round(country_risk / 10, 2),
        "trade_barrier_flag": random.choice(yes_no),
        "route_disruption_flag": random.choice(yes_no),
        "supply_chain_disruption_history": incidents,
        "cybersecurity_incidents": random.randint(0, 3),
        "labor_disputes": random.randint(0, 2),
        
        "risk_score": round(risk_score, 2),
        "criticity_level": target_risk,
        "risk_level": target_risk,
        
        "last_update": (datetime(2025, 11, 18) - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d"),
        "last_assessment_date": (datetime(2025, 11, 18) - timedelta(days=random.randint(0, 90))).isoformat(),
    }

def generate_dataset(n=N):
    print(f"Génération de {n} fournisseurs...")
    data = [generate_supplier(i) for i in range(1, n + 1)]
    df = pd.DataFrame(data)
    
    print(f"\nTotal: {len(df)} fournisseurs")
    print(f"Secteurs: {df['sector'].value_counts().to_dict()}")
    print(f"Niveaux de risque: {df['risk_level'].value_counts().to_dict()}")
    
    return df

def save_dataset(df, output_path="data/raw/suppliers_data.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    
    file_size = os.path.getsize(output_path) / 1024
    print(f"\nFichier sauvegardé: {output_path}")
    print(f"Taille: {file_size:.2f} KB")
    print(f"\nAperçu:")
    print(df.head(3))
    
    return output_path

if __name__ == "__main__":
    df = generate_dataset(n=N)
    save_dataset(df)
    print("\nDataset prêt!")