import socket
import time
import random
import threading

def generate_pressure_value():
    return random.uniform(900, 1100)  # Rastgele basınç değeri

def add_noise(value):
    noise = random.uniform(-5, 5)
    return value + noise

class PressureClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.lock = threading.Lock()

    def fetch_pressure(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)
            while True:
                try:
                    pressure_data = sock.recv(1024)
                    if not pressure_data:
                        break
                    with self.lock:
                        self.last_pressure = float(pressure_data.decode('utf-8'))
                        current_time = int(round(time.time() * 1000))
                        print(f"Pressure Client - {current_time} ms - Received: {self.last_pressure}")
                except Exception as e:
                    print(f"Error receiving pressure data: {e}")
                time.sleep(1)  # 1 saniye aralıklarla server'dan basınç değeri al

    def generate_pressure(self):
        while True:
            with self.lock:
                pressure_value = generate_pressure_value()
                noisy_pressure = add_noise(pressure_value)
                current_time = int(round(time.time() * 1000))
                print(f"Pressure Client - {current_time} ms - New Pressure: {noisy_pressure}")
            time.sleep(1)  # 1 saniye aralıklarla basınç değeri üret

    def run(self):
        pressure_thread = threading.Thread(target=self.fetch_pressure)
        pressure_generation_thread = threading.Thread(target=self.generate_pressure)
        pressure_thread.start()
        pressure_generation_thread.start()
        pressure_thread.join()
        pressure_generation_thread.join()

if __name__ == "__main__":
    server_address = ('localhost', 12345)  # Server adresini ve portunu güncelleyin
    client = PressureClient(server_address)
    client.run()
