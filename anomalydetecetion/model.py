import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from scipy.stats import pearsonr

# Verilerin tanımlanması
basinc = np.array([50.7, 35.63, 98.35, 42.78, 58.67, 55.5, 85.4, 67.23, 63.9, 71.05])
sicaklik = np.array([26.44, 16.2, 49.32, 20.34, 29.335, 30.23, 45.12, 32.1, 28.78, 35.69])
ivme = np.array([5.34, 3.45, 10.45, 4.98, 6.78, 7.01, 5.98, 11.2, 7.8, 5.34])
gyro = np.array([3.12, 2.1, 7.7, 3.33, 5.01, 4.9, 3.87, 7.23, 4.89, 4.7])

# Verilerin birleştirilmesi
X = np.column_stack((basinc, sicaklik, ivme, gyro))

# Rastgele sınıf etiketlerinin oluşturulması
y = np.random.randint(2, size=X.shape[0])

# Modelin oluşturulması
model = Sequential()
model.add(Dense(1, input_dim=4, activation='sigmoid'))

# Modelin derlenmesi
model.compile(loss='binary_crossentropy', optimizer=SGD(), metrics=['accuracy'])

# Modelin eğitilmesi
model.fit(X, y, epochs=100, verbose=1)

# Tahminlerde bulunma
predictions = model.predict(X).flatten()

# Tahmin edilen değerler ile gerçek değerler arasındaki korelasyonun hesaplanması
correlation, _ = pearsonr(predictions, y)
print(f'Korelasyon: {correlation:.4f}')
