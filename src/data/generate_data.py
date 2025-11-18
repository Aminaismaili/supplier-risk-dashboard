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
    """Génère un fournisseur avec toutes ses caractéristiques"""
    country = random.choice(countries)
    sector = random.choice(sectors)
    
    # Métriques de base
    otd = random.uniform(70, 100)
    ppm = int(np.random.lognormal(mean=6, sigma=0.5))
    debt_ratio = random.uniform(0.2, 0.9)
    country_risk = random.randint(10, 90)
    
    # Calcul du score de risque
    risk_score = (
        (100 - otd) / 10 * 0.3 +
        np.log1p(ppm) / 10 * 0.25 +
        debt_ratio * 5 * 0.25 +
        country_risk / 10 * 0.2
    )
    
    # Détermination du niveau de criticité
    if risk_score >= 7:
        criticity_level = "critical"
    elif risk_score >= 5:
        criticity_level = "high"
    elif risk_score >= 3:
        criticity_level = "medium"
    else:
        criticity_level = "low"
    
    return {
        # Identifiants
        "supplier_id": f"F{i:04d}",
        "supplier_name": f"Supplier_{i:04d}",
        "country": country,
        "region": regions[country],
        "sector": sector,
        "family": random.choice(families),
        "single_source": random.choice(yes_no),
        "distance_km": round(random.uniform(50, 1500), 1),
        
        # Infos générales
        "years_in_business": random.randint(1, 50),
        "certification_iso": random.choice(yes_no),
        
        # Données financières
        "revenue_millions": round(np.random.lognormal(mean=3, sigma=1), 2),
        "profit_margin": round(random.uniform(-5, 20), 2),
        "debt_ratio": round(debt_ratio, 3),
        "liquidity_ratio": round(random.uniform(0.5, 2.5), 2),
        "payment_delay_days": random.randint(0, 30),
        "financial_health_score": round(random.uniform(0, 10), 2),
        
        # Performance opérationnelle 3 mois
        "otd_3m": round(otd, 1),
        "avg_delay_days_3m": round(random.uniform(0, 6), 1),
        "delay_volatility_3m": round(random.uniform(0.3, 2.5), 2),
        
        # Performance opérationnelle 6 mois
        "otd_6m": round(random.uniform(70, 100), 1),
        "avg_delay_days_6m": round(random.uniform(0, 6), 1),
        "on_time_delivery_rate": round(otd, 2),
        "lead_time_days": random.randint(5, 60),
        
        # Indicateurs qualité
        "ppm_3m": ppm,
        "defect_rate_3m": round(random.uniform(0.2, 6), 2),
        "quality_defect_rate": round(random.uniform(0.2, 6), 2),
        "cpk_latest": round(random.uniform(0.9, 1.6), 2),
        "recurring_8d": random.randint(0, 7),
        "capacity_utilization": round(random.uniform(50, 100), 2),
        
        # Certifications
        "cert_iatf16949": random.choice(yes_no),
        "iatf_16949": random.choice(yes_no) if sector == "automotive" else "no",
        "cert_as9100": random.choice(yes_no),
        "as9100": random.choice(yes_no) if sector == "aeronautic" else "no",
        "cert_expiry_next90d": random.choice(yes_no),
        "reach_compliance": random.choice(["yes"] * 9 + ["no"]),
        "esg_score": round(random.uniform(40, 95), 1),
        "environmental_score": round(random.uniform(4, 9), 2),
        "non_conformity_flag": random.choice(yes_no),
        
        # Risques externes
        "country_risk_index": country_risk,
        "geopolitical_risk": round(country_risk / 10, 2),
        "trade_barrier_flag": random.choice(yes_no),
        "route_disruption_flag": random.choice(yes_no),
        "supply_chain_disruption_history": random.randint(0, 5),
        "cybersecurity_incidents": random.randint(0, 3),
        "labor_disputes": random.randint(0, 2),
        
        # Évaluation finale
        "risk_score": round(risk_score, 2),
        "criticity_level": criticity_level,
        "risk_level": criticity_level,
        
        # Dates
        "last_update": (datetime(2025, 11, 18) - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d"),
        "last_assessment_date": (datetime(2025, 11, 18) - timedelta(days=random.randint(0, 90))).isoformat(),
    }

def generate_dataset(n=N):
    """Génère le dataset complet"""
    print(f"Génération de {n} fournisseurs...")
    data = [generate_supplier(i) for i in range(1, n + 1)]
    df = pd.DataFrame(data)
    
    # Affichage des stats
    print(f"\nTotal: {len(df)} fournisseurs")
    print(f"Secteurs: {df['sector'].value_counts().to_dict()}")
    print(f"Niveaux de risque: {df['risk_level'].value_counts().to_dict()}")
    
    return df

def save_dataset(df, output_path="data/raw/suppliers_data.csv"):
    """Sauvegarde le dataset en CSV"""
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
