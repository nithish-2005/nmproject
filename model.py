# model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Create dummy training data
def generate_training_data(samples=500):
    data = {
        'vibration': np.random.uniform(0, 10, samples),
        'strain': np.random.uniform(0, 500, samples),
        'temperature': np.random.uniform(20, 80, samples),
    }
    df = pd.DataFrame(data)
    df['status'] = df.apply(lambda row: classify(row), axis=1)
    return df

# Simple rule-based labeling
def classify(row):
    if row['vibration'] > 8 or row['strain'] > 400:
        return 'Critical'
    elif row['vibration'] > 5 or row['strain'] > 250:
        return 'Warning'
    else:
        return 'Safe'

# Train model
def train_model():
    df = generate_training_data()
    X = df[['vibration', 'strain', 'temperature']]
    y = df['status']
    model = RandomForestClassifier()
    model.fit(X, y)
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("✅ Model trained and saved as model.pkl")

if __name__ == "__main__":
    train_model()
