# data_generator.py
import random
import time

def generate_sensor_data():
    return {
        'vibration': random.uniform(0, 10),
        'strain': random.uniform(0, 500),
        'temperature': random.uniform(20, 80)
    }

if __name__ == "__main__":
    while True:
        print(generate_sensor_data())
        time.sleep(1)
 