# model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pickle

# Create dummy training data
def generate_training_data(samples=1000):
    data = {
        'vibration': np.random.uniform(0, 10, samples),
        'strain': np.random.uniform(0, 500, samples),
        'temperature': np.random.uniform(20, 80, samples),
        'humidity': np.random.uniform(30, 90, samples),
        'pressure': np.random.uniform(950, 1050, samples)
    }
    df = pd.DataFrame(data)
    df['status'] = df.apply(lambda row: classify(row), axis=1)
    return df

# Rule-based labeling
def classify(row):
    if row['vibration'] > 8 or row['strain'] > 400 or row['humidity'] > 85 or row['pressure'] > 1040:
        return 'Critical'
    elif row['vibration'] > 5 or row['strain'] > 250 or row['humidity'] > 70:
        return 'Warning'
    else:
        return 'Safe'

# Train both models
def train_models():
    df = generate_training_data()
    X = df[['vibration', 'strain', 'temperature', 'humidity', 'pressure']]
    y = df['status']

    # Random Forest Model
    rf_model = RandomForestClassifier()
    rf_model.fit(X, y)
    with open('rf_model.pkl', 'wb') as f:
        pickle.dump(rf_model, f)
    
    # SVM Model
    svm_model = SVC(probability=True)
    svm_model.fit(X, y)
    with open('svm_model.pkl', 'wb') as f:
        pickle.dump(svm_model, f)

    print("✅ Models trained and saved: rf_model.pkl, svm_model.pkl")

if __name__ == "__main__":
    train_models()
