from flask import Flask, jsonify,render_template
import RPi.GPIO as GPIO
import time
import threading
from flask_socketio import SocketIO, emit,send
from flask_cors import CORS
import datetime
import json



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,async_mode='threading',cors_allowed_origins="*")

connections = 0

data_sent={
    "sensor":"ultrasonic",
    "value":"data",
    "time": datetime.datetime.now()
}

@socketio.on('connect')
def handle_connect():
    global connections
    connections += 1
    print('connected')

@socketio.on('disconnect')
def handle_disconnect():
    global connections
    connections -= 1

# Configura los pines de TRIGGER y ECHO
TRIGGER_PIN = 23
ECHO_PIN = 24
distance = 0
# Configura los pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Envia un pulso de 10us para iniciar la medición
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)
    isTimeout=False
    # Espera a que el pin ECHO esté en HIGH
    start_time = time.time()
    timeout = start_time + 5  # Set the timeout to 5 seconds from the start time
    
    while GPIO.input(ECHO_PIN) == 0:
        if time.time() > timeout:
            isTimeout=True
            break  # Exit the loop if the timeout has been reached
        else:
            start_time = time.time()  # Update the start time if the pin changes state

    # Espera a que el pin ECHO esté en LOW
    if isTimeout:
        return 0.0
 
    stop_time = time.time()
    timeout = stop_time + 5
    while GPIO.input(ECHO_PIN) == 1:
        if time.time() > timeout:
            isTimeout=True
            break  # Exit the loop if the timeout has been reached
        else:
            stop_time = time.time()
    
    if isTimeout:
        return 0.0
    # Calcula la distancia
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2

    return distance

    # ...



def distance_thread():
    global distance
    while True:
        print('enviando...')
        distance = get_distance()
        # Do something with the distance, such as storing it in a global variable or sending it to another function
        
        if connections > 0:
            print('enviando...')
            data_sent["value"]=distance
            data_sent['time']=str(datetime.datetime.now())
            socketio.emit('device-data', json.dumps(data_sent))
        
        time.sleep(3)  # Adjust the sleep duration as needed

# Start the distance thread
th = threading.Thread(target=distance_thread)
#th.daemon = True  # Set the thread as a daemon so it exits when the main program ends
th.start()

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    emit('response', 'This is a response')

# Define the send_data method
def send_data(data):
    socketio.emit('device-data', data)

# Call the send_data method with the distance value


@app.route('/distance', methods=['GET'])
def distance():
    distance = get_distance()
    return jsonify({'distance': distance})

@app.route('/')
def index():
    return render_template('ultrasonicofront.html')

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@app.route('/test')
def index2():
    return "hola mundo"

@socketio.on('message')
def handle_message(data):
    print('received message: ' + str(data))
    socketio.emit('response', 'This is a response')
    socketio.emit('device-data', 'This is a response')

if __name__ == '__main__':
    socketio.run(app,debug=True)
    #app.run(host='0.0.0.0', port=5000,debug=True)