import socket
import time
import random
import threading

def generate_noise():
    return random.uniform(-0.1, 0.1)

class GyroClient:
    def __init__(self, server_address, coefficient):
        self.server_address = server_address
        self.coefficient = coefficient
        self.last_pressure = None
        self.lock = threading.Lock()

    def fetch_pressure(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)
            while True:
                pressure_data = sock.recv(1024)
                if not pressure_data:
                    break
                with self.lock:
                    self.last_pressure = float(pressure_data.decode('utf-8'))
                    current_time = int(round(time.time() * 1000))
                    print(f"Gyro Client - {current_time} ms - Received Pressure: {self.last_pressure}")
                time.sleep(1)  # 1 saniye aralıklarla server'dan basınç değeri al

    def generate_gyro_150ms(self):
        while True:
            with self.lock:
                if self.last_pressure is not None:
                    current_time = int(round(time.time() * 1000))
                    noise = generate_noise()
                    gyro_value = (self.coefficient + noise) * self.last_pressure + generate_noise()
                    print(f"Gyro Client - {current_time} ms - New Gyro (150ms): {gyro_value}")
            time.sleep(0.15)  # 150 ms aralıklarla gyro değeri üret

    def generate_gyro_1s(self):
        while True:
            with self.lock:
                if self.last_pressure is not None:
                    current_time = int(round(time.time() * 1000))
                    noise = generate_noise()
                    gyro_value = (self.coefficient + noise) * self.last_pressure + generate_noise()
                    print(f"Gyro Client - {current_time} ms - New Gyro (1s): {gyro_value}")
            time.sleep(1)  # 1 saniye aralıklarla gyro değeri üret

    def run(self):
        pressure_thread = threading.Thread(target=self.fetch_pressure)
        gyro_150ms_thread = threading.Thread(target=self.generate_gyro_150ms)
        gyro_1s_thread = threading.Thread(target=self.generate_gyro_1s)
        
        pressure_thread.start()
        gyro_150ms_thread.start()
        gyro_1s_thread.start()
        
        pressure_thread.join()
        gyro_150ms_thread.join()
        gyro_1s_thread.join()

if __name__ == "__main__":
    server_address = ('localhost', 10000)  # Server'ın IP adresi ve portu
    coefficient = 0.5
    client = GyroClient(server_address, coefficient)
    client.run()
