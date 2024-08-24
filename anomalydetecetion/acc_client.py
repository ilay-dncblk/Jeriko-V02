import socket
import time
import random
import threading

def generate_noise():
    return random.uniform(-0.1, 0.1)

class AccelerationClient:
    def __init__(self, server_address, coefficient):
        self.server_address = server_address
        self.coefficient = coefficient
        self.last_pressure = None
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
                        print(f"Acceleration Client - {current_time} ms - Received: {self.last_pressure}")
                except Exception as e:
                    print(f"Error receiving pressure data: {e}")
                time.sleep(1)  # 1 saniye aralıklarla server'dan basınç değeri al

    def generate_acceleration(self):
        while True:
            with self.lock:
                if self.last_pressure is not None:
                    current_time = int(round(time.time() * 1000))
                    noise = generate_noise()
                    acceleration_value = (self.coefficient + noise) * self.last_pressure + generate_noise()
                    print(f"Acceleration Client - {current_time} ms - New Acceleration: {acceleration_value}")
            time.sleep(0.2)  # 200 ms aralıklarla ivme değeri üret

    def run(self):
        pressure_thread = threading.Thread(target=self.fetch_pressure)
        acceleration_thread = threading.Thread(target=self.generate_acceleration)
        pressure_thread.start()
        acceleration_thread.start()
        pressure_thread.join()
        acceleration_thread.join()

if __name__ == "__main__":
    server_address = ('localhost', 12345)  # Server adresini ve portunu güncelleyin
    coefficient = 0.5
    client = AccelerationClient(server_address, coefficient)
    client.run()
