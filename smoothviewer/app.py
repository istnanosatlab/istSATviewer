"""
Simple script that will create a webserver. Conenct to satViewer and will display the received data inside the browser
"""
from flask import Flask, render_template, jsonify
import threading
import socket
import time
import json
import yaml
import re

app = Flask(__name__)

dataDict = {}
size = 4096  # Initial size of the buffer to receive data from the sender server


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

    buffer = ""
    stack = []

    while True:
        received_data = client_socket.recv(size).decode('utf-8')
        if not received_data:
            break

        # Read the received data and check when to stop since its a json has a determined pattern
        buffer += received_data
        for char in received_data:
            if char == '{':
                stack.append('{')
            elif char == '}':
                if stack:
                    stack.pop()
                if not stack:
                    try:
                        dataDict = json.loads(buffer)
                        buffer = "" 
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")
                        buffer = "" 


# Function to read the units from the yaml file
def read_units(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Function to read the descriptions from the yaml file
def read_descriptions(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


units_file = read_units('../units.yml')
descriptions_file = read_descriptions('../istsat.yml')


# Function to parse the expression 10^x
def parse_exp(expression):
    return re.sub(r'\.10\^(-?\d+)', r'.10<sup>\1</sup>', expression)


# Function to add units to the data
def add_units_to_data(data, units):
    for category, fields in units.items():
        if category in data:
            for field, unit in fields.items():
                if field in data[category]:
                    data[category][field] = f"{data[category][field]} {parse_exp(unit)}"

    common_fields = units.get('COMMON', {})
    for category in data:
        for field, unit in common_fields.items():
            if field in data[category]:
                data[category][field] = f"{data[category][field]} {parse_exp(unit)}"
    return data


# Function to add descriptions to the data
def add_descriptions_to_data(data, descriptions):
    subsystems = descriptions.get('subsystems', {})
    for category, content in subsystems.items():
        if category in data:
            for field, info in content.get('data', {}).items():
                if field in data[category]:
                    data[category][field] = {"value": data[category][field], "doc": info.get('doc', 'No description available')}

    common_fields = subsystems.get('COMMON', {}).get('data', {})
    for category in data:
        for field, info in common_fields.items():
            if field in data[category]:
                data[category][field] = {"value": data[category][field], "doc": info.get('doc', 'No description available')}
    return data


# Function to check if the data needs to be updated
def needs_update(data):
        for category in data.values():
            for field in category.values():
                if not isinstance(field, dict) or 'value' not in field or 'doc' not in field:
                    return True
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data', methods=['GET'])
def get_data():
    global dataDict
    current_data = dataDict
    if needs_update(current_data):
        data_with_units = add_units_to_data(current_data, units_file)
        data_with_descriptions = add_descriptions_to_data(data_with_units, descriptions_file)
    else:
        data_with_descriptions = current_data
    return jsonify(data_with_descriptions)


if __name__ == '__main__':
    # create another thread
    t = threading.Thread(target=receive_data)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
