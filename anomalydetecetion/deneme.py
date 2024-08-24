import pandas as pd

data = pd.read_csv('IMU_Data_1(No Mag).csv')

# Gereksiz sütunları sil
columns_to_drop = ['Gyro_y', 'Gyro_z', 'Acc_y', 'Acc_z',  'Euler_y', 'Euler_z', 'Quat_1', 'Quat_2', 'Quat_3']
data.drop(columns=columns_to_drop, inplace=True)



# Yeni DataFrame'i yeni bir CSV dosyasına yaz
output_file_path = 'combined_data.csv'
data.to_csv(output_file_path, index=False)

print(f"Birleştirilmiş veriler {output_file_path} dosyasına yazıldı.")
