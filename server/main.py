from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin_avancer = 23
pin_reculer = 24
pin_tourner_gauche = 17
pin_tourner_droite = 27

GPIO.setup(pin_avancer, GPIO.OUT)
GPIO.setup(pin_reculer, GPIO.OUT)
GPIO.setup(pin_tourner_gauche, GPIO.OUT)
GPIO.setup(pin_tourner_droite, GPIO.OUT)

def control_gpio(pin, duration=1):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)

@app.route('/avancer', methods=['POST'])
def avancer():
    duration = request.json.get('duration', 1)
    control_gpio(pin_avancer, duration)
    return "Avancé pendant {} secondes".format(duration)

@app.route('/reculer', methods=['POST'])
def reculer():
    duration = request.json.get('duration', 1)
    control_gpio(pin_reculer, duration)
    return "Reculé pendant {} secondes".format(duration)

@app.route('/tourner/gauche', methods=['POST'])
def tourner_gauche():
    duration = request.json.get('duration', 1)
    control_gpio(pin_tourner_gauche, duration)
    return "Tourné à gauche pendant {} secondes".format(duration)

@app.route('/tourner/droite', methods=['POST'])
def tourner_droite():
    duration = request.json.get('duration', 1)
    control_gpio(pin_tourner_droite, duration)
    return "Tourné à droite pendant {} secondes".format(duration)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
