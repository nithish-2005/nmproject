# app.py
from flask import Flask, render_template, jsonify
import random
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open('model.pkl', 'rb'))

# Generate random sensor data
def generate_sensor_data():
    return {
        'vibration': random.uniform(0, 10),
        'strain': random.uniform(0, 500),
        'temperature': random.uniform(20, 80)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor-data')
def sensor_data():
    data = generate_sensor_data()
    features = np.array([[data['vibration'], data['strain'], data['temperature']]])
    prediction = model.predict(features)[0]
    data['status'] = prediction
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
