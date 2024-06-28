"""
Simple script that will create a webserver. Conenct to satViewer and will display the received data inside the browser
"""

from flask import Flask, render_template, jsonify
import threading
import socket
import time
import json

app = Flask(__name__)

dataDict = {}



def connect_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12400))
        return client_socket
    except Exception as e:
        print("Could not connect to sender server: ", e)
        print("  Trying again in 5 seconds...")
        return None


# Function to handle receiving data from the sender server
def receive_data():
    global dataDict
    client_socket = None
    
    while client_socket is None:
        client_socket = connect_server()
        time.sleep(5)

    while True:
        received_data = client_socket.recv(4096)
        if not received_data:
            break
        dataDict = json.loads(received_data.decode('utf-8'))
    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    global dataDict
    current_data = dataDict
    return jsonify(current_data)

if __name__ == '__main__':

    # create another thread
    t = threading.Thread(target=receive_data)
    t.start()

    app.run(debug=False)
