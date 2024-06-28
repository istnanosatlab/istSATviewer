"""
This is a simple script to test the functionaly of the webserver. It will create the server and generate data to send to the website
"""
import socket
import json
import time
import threading
import random



data = {
    "temperature": "22C",
    "humidity": "60%",
    "pressure": "1013hPa"
}

active_threads = {}
thread_lock = threading.Lock()
server_running = True

def generateData():
    return {
        "temperature": f"{random.randint(0, 100)}C",
        "humidity": f"{random.randint(0, 100)}%",
        "pressure": f"{random.randint(1000, 2000)}hPa"
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