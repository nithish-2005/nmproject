# app.py
from flask import Flask, render_template, jsonify, send_file
import random
import pickle
import numpy as np
import smtplib
from email.message import EmailMessage
from fpdf import FPDF
import os

app = Flask(__name__)

# Load AI Models
rf_model = pickle.load(open('rf_model.pkl', 'rb'))
svm_model = pickle.load(open('svm_model.pkl', 'rb'))

# Generate random sensor data
def generate_sensor_data():
    return {
        'vibration': random.uniform(0, 10),
        'strain': random.uniform(0, 500),
        'temperature': random.uniform(20, 80),
        'humidity': random.uniform(30, 90),
        'pressure': random.uniform(950, 1050)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor-data')
def sensor_data():
    data = generate_sensor_data()
    features = np.array([[data['vibration'], data['strain'], data['temperature'], data['humidity'], data['pressure']]])
    prediction = rf_model.predict(features)[0]  # Using Random Forest model for now
    data['status'] = prediction

    # Store latest data for PDF download
    global latest_data
    latest_data = data

    return jsonify(data)

@app.route('/send-email')
def send_email():
    try:
        email_sender = 'nithnithish500@gmail.com'   # <-- Change to your Gmail
        email_password = '110466'    # <-- App password, not Gmail login password
        email_receiver = 'nitintech6@gmail.com' # <-- Change to where you want to send alert

        subject = '🚨 Critical Structural Health Alert!'
        body = f'''
        ALERT!

        Critical structural condition detected.

        Latest Sensor Data:
        Vibration: {latest_data['vibration']}
        Strain: {latest_data['strain']}
        Temperature: {latest_data['temperature']}
        Humidity: {latest_data['humidity']}
        Pressure: {latest_data['pressure']}
        Status: {latest_data['status']}
        '''

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
        
        return "Email Sent!"
    except Exception as e:
        print("Email Error:", e)
        return "Email Failed!"

@app.route('/download-pdf')
def download_pdf():
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Structural Health Report", ln=True, align='C')
        pdf.ln(10)
        
        for key, value in latest_data.items():
            pdf.cell(200, 10, txt=f"{key.capitalize()}: {value}", ln=True)

        pdf_file = 'report.pdf'
        pdf.output(pdf_file)

        return send_file(pdf_file, as_attachment=True)
    except Exception as e:
        print("PDF Error:", e)
        return "PDF Download Failed!"

if __name__ == '__main__':
    app.run(debug=True)
