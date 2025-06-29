import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt

# Path dataset
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'media', 'resi')

print("DATA_DIR:", DATA_DIR)

# Parameter training
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 8
EPOCHS = 10

# Data preprocessing (tanpa validasi)
datagen = ImageDataGenerator(
    rescale=1./255
)

# Generator training
train_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Model CNN
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Training model & simpan history
history = model.fit(
    train_generator,
    epochs=EPOCHS
)

# Simpan model
model.save(os.path.join(BASE_DIR, 'media', 'model_resi_cnn.h5'))

# Cetak akurasi terakhir
train_acc = history.history['accuracy'][-1]
print(f"Akurasi Training Terakhir: {train_acc:.2f}")

# Plot grafik akurasi
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training Accuracy')
plt.legend()
plt.grid()
plt.show()
