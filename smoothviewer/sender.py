"""
This is a simple script to test the functionaly of the webserver. It will create the server and generate data to send to the website
"""
import socket
import json
import time
import threading
import random

"""
Example of data that will be sent to the client

data = {
    "OBC": {
              "time": {value: 22 uV, doc: tempertatura quando x e y}, 
              "temperature": {value: 22ºC, doc: tempertatura quando x e y}, 
              "humidity": {value: 22, doc: tempertatura quando x e y}, 
              "pressure": {value: 22, doc: tempertatura quando x e y}
         },
    "EPS": {
              "time": {value: 22, doc: tempertatura quando x e y},
              "temperature": {value: 22, doc: tempertatura quando x e y},
              "humidity": {value: 22, doc: tempertatura quando x e y},
              "pressure": {value: 22, doc: tempertatura quando x e y}
         },
    "TTC": {
              "time": {value: 22, doc: tempertatura quando x e y},
              "temperature": {value: 22, doc: tempertatura quando x e y},
              "humidity": {value: 22, doc: tempertatura quando x e y},
              "pressure": {value: 22, doc: tempertatura quando x e y}
         }
}
"""

data = {
    "OBC": {
        "time_boot": 44223,
        "time_ot": 2466919,
        "hk_scmode": 2,
        "adcs_state": 2,
        "adcs_gyro_x": -4450248,
        "adcs_gyro_y": 2815915,
        "adcs_gyro_z": -2728914,
        "adcs_mag_B_x": 314708,
        "adcs_mag_B_y": -303204,
        "adcs_mag_B_z": -24336,
        "adcs_quat_x": 1000000000,
        "adcs_quat_y": 0,
        "adcs_quat_z": 0,
        "adcs_quat_w": 0,
        "adcs_sunsensor_xplus": 185347,
        "adcs_sunsensor_xminus": 1493040,
        "adcs_sunsensor_yplus": 745784,
        "adcs_sunsensor_yminus": 1493040,
        "adcs_sunsensor_zplus": 1493040,
        "temperature": 32442,
        "temperature1": 32000,
        "hk_mon_ttc_status": 3,
        "hk_mon_eps_status": 3,
        "hk_mon_com_status": 3,
        "hk_mon_pl_status": 3
    },
    "EPS": {
        "time_boot": 44223,
        "hk_scmode": 2,
        "vcc0_voltage": 3300000,
        "vcc1_voltage": 3300000,
        "vcc2_voltage": 3300000,
        "vcc3_voltage": 3300000,
        "buses_voltage": 3300000,
        "v3_3_voltage": 3300000,
        "battery_voltage": 3300000,
        "battery_current": 100,
        "battery_heater_en": 1,
        "battery_temperature1": 32,
        "battery_temperature2": 32,
        "battery_temperature3": 32,
        "battery_temperature4": 32,
        "eps_temperature": 32,
        "micro_temperature": 32,
        "battery_charge_raw": 100,
        "battery_charge": 100
    },
    "TTC": {
        "time_boot": 44223,
        "hk_scmode": 2,
        "ax25_tx_msgs": 1004,
        "ax25_rx_msgs": 230,
        "antenna_switch_status": 1,
        "error_status": 0,
        "carrier_sense": 1,
        "temp_adm": 32
    }
}

active_threads = {}
thread_lock = threading.Lock()
server_running = True


def generateData():
    return {
        "OBC": {
            "time_boot": 123434324,
            "time_ot": 123434324,
            "hk_scmode": 2,
            "adcs_state": 2,
            "adcs_gyro_x": random.randint(-5, 10),
            "adcs_gyro_y": random.randint(-5, 10),
            "adcs_gyro_z": random.randint(-5, 10),
            "adcs_mag_B_x": random.randint(-5, 10),
            "adcs_mag_B_y": random.randint(-5, 10),
            "adcs_mag_B_z": random.randint(-5, 10),
            "adcs_quat_x": random.randint(-5, 10),
            "adcs_quat_y": random.randint(-5, 10),
            "adcs_quat_z": random.randint(-5, 10),
            "adcs_quat_w": random.randint(-5, 10),
            "adcs_sunsensor_xplus": random.randint(-5, 10),
            "adcs_sunsensor_xminus": random.randint(-5, 10),
            "adcs_sunsensor_yplus": random.randint(-5, 10),
            "adcs_sunsensor_yminus": random.randint(-5, 10),
            "adcs_sunsensor_zplus": random.randint(-5, 10),
            "temperature": random.randint(-10, 60),
            "temperature1": random.randint(-10, 60),
            "hk_mon_ttc_status": 3,
            "hk_mon_eps_status": 3,
            "hk_mon_com_status": 3,
            "hk_mon_pl_status": 3
        },
        "EPS": {
            "time_boot": 123434324,
            "hk_scmode": 2,
            "vcc0_voltage": random.randint(0, 20),
            "vcc1_voltage": random.randint(0, 20),
            "vcc2_voltage": random.randint(0, 20),
            "vcc3_voltage": random.randint(0, 20),
            "buses_voltage": random.randint(0, 20),
            "v3_3_voltage": random.randint(0, 20),
            "battery_voltage": random.randint(0, 20),
            "battery_current": random.randint(0, 20),
            "battery_heater_en": 1,
            "battery_temperature1": random.randint(-10, 60),
            "battery_temperature2": random.randint(-10, 60),
            "battery_temperature3": random.randint(-10, 60),
            "battery_temperature4": random.randint(-10, 60),
            "eps_temperature": random.randint(-10, 60),
            "micro_temperature": random.randint(-10, 60),
            "battery_charge_raw": random.randint(0, 100),
            "battery_charge": random.randint(0, 100)
        },
        "TTC": {
            "time_boot": 123434324,
            "hk_scmode": 2,
            "ax25_tx_msgs": random.randint(0, 100),
            "ax25_rx_msgs": random.randint(0, 100),
            "antenna_switch_status": 1,
            "error_status": 0,
            "carrier_sense": 1,
            "temp_adm": random.randint(-10, 60)
        }
    }

def send_data(client_socket, thread_id):
    global active_threads
    while server_running:
        try:
            data = generateData()
            client_socket.sendall(json.dumps(data).encode('utf-8'))
            with thread_lock:
                active_threads[thread_id] = time.time()
            time.sleep(5)  # Send data every 5 seconds
        except (BrokenPipeError, ConnectionResetError):
            break
    with thread_lock:
        active_threads.pop(thread_id, None)
    client_socket.close()

def start_server():
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12400))
    server_socket.listen(5)
    print("Sender server listening on port 1234")

    while server_running:
        try:
            client_socket, addr = server_socket.accept()
            print('Connected by', addr)
            thread_id = addr
            with thread_lock:
                active_threads[thread_id] = time.time()
            threading.Thread(target=send_data, args=(client_socket, thread_id)).start()
        except socket.error as e:
            print(f"Socket error: {e}")
            break

def watchdog():
    global active_threads
    while server_running:
        current_time = time.time()
        with thread_lock:
            for thread_id, last_active in list(active_threads.items()):
                if current_time - last_active > 300:  # 5 minutes
                    print(f"Thread {thread_id} inactive for more than 5 minutes, terminating.")
                    active_threads.pop(thread_id, None)
        time.sleep(60)  # Check every minute

def signal_handler(sig, frame):
    global server_running
    print('Shutting down gracefully...')
    server_running = False
    with thread_lock:
        for thread_id in list(active_threads.keys()):
            print(f"Terminating thread {thread_id}")
            # Force close threads if needed
            # For a better approach, you may want to join threads or clean up any resources
    exit(0)

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C

    # Start the watchdog thread
    threading.Thread(target=watchdog, daemon=True).start()
    try:
        start_server()
    except Exception as e:
        print(f"Server encountered an error: {e}")
    finally:
        print("Server has shut down.")