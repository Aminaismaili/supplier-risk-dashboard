import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
import mlflow
import mlflow.sklearn
import joblib
import os
from datetime import datetime

class RiskPredictionBenchmark:
    
    def __init__(self, experiment_name="supplier_risk_prediction"):
        self.models = {}
        self.results = {}
        self.best_model = None
        self.label_encoder = LabelEncoder()
        
        mlflow.set_experiment(experiment_name)
        
    def load_data(self, data_path='data/processed/suppliers_processed.csv'):
        print(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        
        X = df.drop('risk_level', axis=1)
        y = df['risk_level']
        
        y_encoded = self.label_encoder.fit_transform(y)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        print(f"Train set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def initialize_models(self):
        self.models = {
            'logistic_regression': LogisticRegression(max_iter=1000, random_state=42),
            
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            ),
            
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            
            'xgboost': XGBClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
                eval_metric='mlogloss'
            ),
            
            'svm': SVC(
                kernel='rbf',
                C=1.0,
                random_state=42,
                probability=True
            )
        }
        
        print(f"Initialized {len(self.models)} models")
    
    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        
        for model_name, model in self.models.items():
            print(f"\n{'='*60}")
            print(f"Training: {model_name}")
            print(f"{'='*60}")
            
            with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
                
                mlflow.log_param("model_type", model_name)
                mlflow.log_param("train_size", len(X_train))
                mlflow.log_param("test_size", len(X_test))
                
                model.fit(X_train, y_train)
                
                y_pred = model.predict(X_test)
                
                accuracy = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
                cv_mean = cv_scores.mean()
                cv_std = cv_scores.std()
                
                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("f1_score", f1)
                mlflow.log_metric("cv_mean", cv_mean)
                mlflow.log_metric("cv_std", cv_std)
                
                mlflow.sklearn.log_model(model, model_name)
                
                self.results[model_name] = {
                    'accuracy': accuracy,
                    'f1_score': f1,
                    'cv_mean': cv_mean,
                    'cv_std': cv_std,
                    'model': model
                }
                
                print(f"Accuracy: {accuracy:.4f}")
                print(f"F1 Score: {f1:.4f}")
                print(f"CV Mean: {cv_mean:.4f} (+/- {cv_std:.4f})")
                
                print("\nClassification Report:")
                print(classification_report(
                    y_test, y_pred, 
                    target_names=self.label_encoder.classes_
                ))
    
    def select_best_model(self):
        best_score = 0
        best_name = None
        
        print(f"\n{'='*60}")
        print("BENCHMARK RESULTS")
        print(f"{'='*60}")
        
        for model_name, metrics in self.results.items():
            print(f"\n{model_name}:")
            print(f"  Accuracy: {metrics['accuracy']:.4f}")
            print(f"  F1 Score: {metrics['f1_score']:.4f}")
            print(f"  CV Mean:  {metrics['cv_mean']:.4f}")
            
            if metrics['f1_score'] > best_score:
                best_score = metrics['f1_score']
                best_name = model_name
        
        self.best_model = self.results[best_name]['model']
        
        print(f"\n{'='*60}")
        print(f"BEST MODEL: {best_name}")
        print(f"F1 Score: {best_score:.4f}")
        print(f"{'='*60}")
        
        return best_name, self.best_model
    
    def save_best_model(self, model_name, output_dir='models'):
        os.makedirs(output_dir, exist_ok=True)
        
        joblib.dump(self.best_model, f'{output_dir}/best_model.pkl')
        joblib.dump(self.label_encoder, f'{output_dir}/label_encoder.pkl')
        
        with open(f'{output_dir}/best_model_info.txt', 'w') as f:
            f.write(f"Best Model: {model_name}\n")
            f.write(f"Metrics: {self.results[model_name]}\n")
        
        print(f"\nBest model saved to {output_dir}/")


def main():
    print("Starting ML Benchmark Pipeline...")
    
    benchmark = RiskPredictionBenchmark()
    
    X_train, X_test, y_train, y_test = benchmark.load_data()
    
    benchmark.initialize_models()
    
    benchmark.train_and_evaluate(X_train, X_test, y_train, y_test)
    
    best_name, best_model = benchmark.select_best_model()
    
    benchmark.save_best_model(best_name)
    
    print("\nBenchmark completed successfully!")


if __name__ == "__main__":
    main()