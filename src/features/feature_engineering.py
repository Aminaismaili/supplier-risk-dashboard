import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import os

class FeatureEngineer:
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='median')
        
    def create_features(self, df):
        df = df.copy()
        
        # Financial composite features
        df['revenue_per_year'] = df['revenue_millions'] / np.maximum(df['years_in_business'], 1)
        df['financial_stability'] = (
            (df['financial_health_score'] * 0.4) +
            ((1 - df['debt_ratio']) * 5 * 0.3) +
            (df['profit_margin'] * 0.3)
        )
        
        # Operational composite features
        df['operational_excellence'] = (
            (df['on_time_delivery_rate'] * 0.5) +
            ((100 - df['quality_defect_rate'] * 10).clip(0, 100) * 0.3) +
            (df['capacity_utilization'] * 0.2)
        ) / 10
        
        df['logistics_efficiency'] = df['on_time_delivery_rate'] / np.log1p(df['lead_time_days'])
        
        # Maturity features
        df['maturity_score'] = np.clip(df['years_in_business'] / 20, 0, 1) * 10
        df['is_established'] = (df['years_in_business'] >= 10).astype(int)
        df['is_young_company'] = (df['years_in_business'] < 5).astype(int)
        
        # Compliance features
        df['iatf_16949_binary'] = (df['iatf_16949'] == 'yes').astype(int)
        df['as9100_binary'] = (df['as9100'] == 'yes').astype(int)
        df['reach_compliance_binary'] = (df['reach_compliance'] == 'yes').astype(int)
        df['certification_iso_binary'] = (df['certification_iso'] == 'yes').astype(int)
        
        df['certification_count'] = (
            df['certification_iso_binary'] +
            df['iatf_16949_binary'] +
            df['as9100_binary'] +
            df['reach_compliance_binary']
        )
        
        df['has_sector_certification'] = (
            df['iatf_16949_binary'] | df['as9100_binary']
        ).astype(int)
        
        df['compliance_score'] = (
            (df['certification_count'] * 2) +
            (df['environmental_score']) +
            (df['has_sector_certification'] * 2)
        ) / 1.2
        
        # Risk composite features
        df['total_incidents'] = (
            df['supply_chain_disruption_history'] +
            df['cybersecurity_incidents'] +
            df['labor_disputes']
        )
        
        df['external_risk_score'] = (
            (df['geopolitical_risk'] * 0.5) +
            (df['total_incidents'] * 2) +
            ((10 - df['environmental_score']) * 0.3)
        )
        
        # Interaction features
        df['risk_debt_interaction'] = df['debt_ratio'] * df['geopolitical_risk']
        df['quality_delivery_interaction'] = (
            df['quality_defect_rate'] * (100 - df['on_time_delivery_rate'])
        )
        
        # Ratios
        df['debt_to_revenue_ratio'] = df['debt_ratio'] / np.maximum(df['revenue_millions'], 0.1)
        df['profitability_ratio'] = df['profit_margin'] / np.maximum(df['revenue_millions'], 0.1)
        
        return df
    
    def encode_categorical(self, df):
        df = df.copy()
        categorical_cols = ['country', 'region', 'sector', 'family']
        
        for col in categorical_cols:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col + '_encoded'] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col + '_encoded'] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def handle_missing_values(self, df):
        missing = df.isnull().sum()
        if missing.sum() > 0:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = self.imputer.fit_transform(df[numeric_cols])
        
        return df
    
    def prepare_for_ml(self, df):
        exclude_cols = [
            'supplier_id', 'supplier_name', 'risk_level', 'criticity_level',
            'last_update', 'last_assessment_date', 'risk_score',
            'country', 'region', 'sector', 'family',
            'certification_iso', 'iatf_16949', 'as9100', 'reach_compliance',
            'single_source', 'cert_iatf16949', 'cert_as9100', 'cert_expiry_next90d',
            'trade_barrier_flag', 'route_disruption_flag', 'non_conformity_flag'
        ]
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols]
        y = df['risk_level'] if 'risk_level' in df.columns else None
        
        return X, y
    
    def save_transformers(self, output_dir='models'):
        os.makedirs(output_dir, exist_ok=True)
        joblib.dump(self.scaler, f'{output_dir}/scaler.pkl')
        joblib.dump(self.label_encoders, f'{output_dir}/label_encoders.pkl')
        joblib.dump(self.imputer, f'{output_dir}/imputer.pkl')


def preprocess_pipeline(input_path='data/raw/suppliers_data.csv', 
                        output_path='data/processed/suppliers_processed.csv'):
    
    print("Loading data...")
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} suppliers")
    
    fe = FeatureEngineer()
    
    print("Creating features...")
    df = fe.create_features(df)
    
    print("Handling missing values...")
    df = fe.handle_missing_values(df)
    
    print("Encoding categorical variables...")
    df = fe.encode_categorical(df)
    
    print("Preparing for ML...")
    X, y = fe.prepare_for_ml(df)
    
    print("Saving processed data...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    processed_df = X.copy()
    if y is not None:
        processed_df['risk_level'] = y.values
    
    processed_df.to_csv(output_path, index=False)
    fe.save_transformers()
    
    print(f"Done. Final shape: {processed_df.shape}")
    
    return processed_df, fe


if __name__ == "__main__":
    df_processed, feature_engineer = preprocess_pipeline()
    print("\nPreprocessing completed successfully")
    print(f"\nRisk distribution:")
    if 'risk_level' in df_processed.columns:
        print(df_processed['risk_level'].value_counts())