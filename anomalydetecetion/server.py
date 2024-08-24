import socket
import time
import random
import threading

def generate_pressure_value():
    return random.uniform(300, 1100)  # Rastgele basınç değeri (örnek aralık)

def add_noise(value):
    noise = random.uniform(-5, 5)
    return value + noise

def server_program():
    host = 'localhost'
    port = 12345
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(4)

    clients = []

    def accept_clients():
        while True:
            conn, address = server_socket.accept()
            print(f"Connection from: {address}")
            clients.append(conn)

    threading.Thread(target=accept_clients).start()

    while True:
        pressure_value = generate_pressure_value()
        noisy_pressure = add_noise(pressure_value)
        print(f"Generated pressure value: {noisy_pressure}")

        for client in clients:
            try:
                client.sendall(str(noisy_pressure).encode())
            except Exception as e:
                print(f"Error sending data to client: {e}")

        time.sleep(1)

if __name__ == '__main__':
    server_program()
