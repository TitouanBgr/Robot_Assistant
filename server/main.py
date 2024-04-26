from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # ENA
GPIO.setup(18, GPIO.OUT)  # ENB
GPIO.setup(27, GPIO.OUT)  # IN1
GPIO.setup(22, GPIO.OUT)  # IN2
GPIO.setup(23, GPIO.OUT)  # IN3
GPIO.setup(24, GPIO.OUT)  # IN4

# Initialisation des PWM pour le contrôle de vitesse
pwm_a = GPIO.PWM(17, 100)  # PWM pour la vitesse du moteur A
pwm_b = GPIO.PWM(18, 100)  # PWM pour la vitesse du moteur B

def drive_forward():
    GPIO.output(27, GPIO.HIGH)  # IN1
    GPIO.output(22, GPIO.LOW)   # IN2
    GPIO.output(23, GPIO.LOW)   # IN3
    GPIO.output(24, GPIO.HIGH)  # IN4
    pwm_a.start(100)
    pwm_b.start(100)
    time.sleep(1.5) 
    stop()

def drive_backward():
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    pwm_a.start(100)
    pwm_b.start(100)
    time.sleep(1.5) 
    stop()

def turn_left():
    GPIO.output(27, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    pwm_a.start(100)
    pwm_b.start(100)
    time.sleep(1.5) 
    stop()

def turn_right():
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    pwm_a.start(100)
    pwm_b.start(100)
    time.sleep(1.5) 
    stop()

def stop():
    pwm_a.stop()
    pwm_b.stop()
    GPIO.output(17, GPIO.LOW)  # ENA
    GPIO.output(18, GPIO.LOW)  # ENB

@app.route('/avancer', methods=['POST'])
def avancer():
    drive_forward()
    return jsonify(message="Driving forward")

@app.route('/reculer', methods=['POST'])
def reculer():
    drive_backward()
    return jsonify(message="Driving backward")

@app.route('/gauche', methods=['POST'])
def gauche():
    turn_left()
    return jsonify(message="Turning left")

@app.route('/droite', methods=['POST'])
def droite():
    turn_right()
    return jsonify(message="Turning right")

@app.route('/stop', methods=['POST'])
def api_stop():
    stop()
    return jsonify(message="Stopping")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
