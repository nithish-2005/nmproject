from flask import Flask, render_template, jsonify, send_file
import random
import pickle
import numpy as np
import smtplib
from email.message import EmailMessage
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import datetime

app = Flask(__name__)

# Load AI Models
rf_model = pickle.load(open('rf_model.pkl', 'rb'))
svm_model = pickle.load(open('svm_model.pkl', 'rb'))

# Global latest data
latest_data = {}

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
    global latest_data
    data = generate_sensor_data()
    features = np.array([[data['vibration'], data['strain'], data['temperature'], data['humidity'], data['pressure']]])
    prediction = rf_model.predict(features)[0]  # Using Random Forest model
    data['status'] = prediction
    latest_data = data
    return jsonify(data)

@app.route('/send-email')
def send_email():
    try:
        email_sender = 'nithnithish500@gmail.com'  # Change this
        email_password = 'wcheugpbtbut hrfc'   # Change this
        email_receiver = 'nithish2005.vnb@gmail.com'  # Change this

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
        # Random patient details
        patient_number = f"P-{random.randint(1000, 9999)}"
        age = random.randint(20, 60)
        gender = random.choice(["Male", "Female"])
        visited_on = datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p")

        # Create a graph of sensor values
        labels = ['Vibration', 'Strain', 'Temperature', 'Humidity', 'Pressure']
        values = [
            latest_data.get('vibration', 0),
            latest_data.get('strain', 0),
            latest_data.get('temperature', 0),
            latest_data.get('humidity', 0),
            latest_data.get('pressure', 0)
        ]

        plt.figure(figsize=(8, 4))
        plt.plot(labels, values, marker='o')
        plt.title('Sensor Data Graph')
        plt.xlabel('Sensor Type')
        plt.ylabel('Sensor Value')
        plt.grid(True)
        plt.tight_layout()
        graph_path = 'sensor_graph.png'
        plt.savefig(graph_path)
        plt.close()

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Title
        pdf.cell(200, 10, txt="Structural Health Monitoring Report", ln=True, align='C')
        pdf.ln(5)

        # Patient Details
        pdf.cell(200, 10, txt=f"Patient Number: {patient_number}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {age} years", ln=True)
        pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"Visited On: {visited_on}", ln=True)
        pdf.ln(5)

        # Health Status
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(200, 10, txt=f"Status: {latest_data.get('status', 'Unknown')}", ln=True)
        pdf.ln(10)

        # Insert Graph
        if os.path.exists(graph_path):
            pdf.image(graph_path, x=10, y=None, w=190)

        # Save PDF
        report_file = "Structural_Report.pdf"
        pdf.output(report_file)

        # Cleanup
        if os.path.exists(graph_path):
            os.remove(graph_path)

        return send_file(report_file, as_attachment=True)

    except Exception as e:
        print("PDF Error:", e)
        return "PDF generation failed."

if __name__ == '__main__':
    app.run(debug=True)