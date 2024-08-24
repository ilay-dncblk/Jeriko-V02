import threading
import os


def run_script(script_name):
    os.system(f'python {script_name}')


thread1 = threading.Thread(target=run_script, args=('press_client',))
thread2 = threading.Thread(target=run_script, args=('temp_client.py',))
thread3 = threading.Thread(target=run_script, args=('acc_client.py',))
thread4 = threading.Thread(target=run_script, args=('gyro_client.py',))

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()