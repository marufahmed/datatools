import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, BatchNormalization, Activation, Add, AveragePooling2D, Flatten, Dense
from tensorflow.keras.models import Model

# Define constants
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
BATCH_SIZE_PER_GPU = 32
BATCH_SIZE = BATCH_SIZE_PER_GPU * 2  # Total batch size across all GPUs
EPOCHS = 500

# Set the path to your dataset
train_dir = '/kaggle/input/dataset/dataset/Train'
validation_dir = '/kaggle/input/dataset/dataset/Validation'
test_dir = '/kaggle/input/dataset/dataset/Test'

# Define data generators with augmentation for train data
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

validation_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Flow images from directories using data generators
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
                                                    batch_size=BATCH_SIZE,
                                                    class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(validation_dir,
                                                              target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
                                                              batch_size=BATCH_SIZE,
                                                              class_mode='binary')

test_generator = test_datagen.flow_from_directory(test_dir,
                                                  target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
                                                  batch_size=BATCH_SIZE,
                                                  class_mode='binary')

# Residual block for ResNet
def residual_block(x, filters, kernel_size=3, strides=1, activation='relu'):
    y = Conv2D(filters, kernel_size, strides=strides, padding='same')(x)
    y = BatchNormalization()(y)
    y = Activation(activation)(y)

    y = Conv2D(filters, kernel_size, padding='same')(y)
    y = BatchNormalization()(y)

    if strides > 1:
        x = Conv2D(filters, 1, strides=strides, padding='same')(x)

    out = Add()([x, y])
    out = Activation(activation)(out)
    return out

# ResNet-18 architecture
def ResNet18(input_shape, num_classes):
    inputs = Input(shape=input_shape)

    x = Conv2D(64, 7, strides=2, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(3, strides=2, padding='same')(x)

    x = residual_block(x, 64)
    x = residual_block(x, 64)

    x = residual_block(x, 128, strides=2)
    x = residual_block(x, 128)

    x = residual_block(x, 256, strides=2)
    x = residual_block(x, 256)

    x = residual_block(x, 512, strides=2)
    x = residual_block(x, 512)

    x = AveragePooling2D(4)(x)
    x = Flatten()(x)
    outputs = Dense(num_classes, activation='sigmoid')(x)

    model = Model(inputs, outputs)
    return model

# Build ResNet-18 model
model = ResNet18((IMAGE_WIDTH, IMAGE_HEIGHT, 3), num_classes=1)

# Compile model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train model
history = model.fit(train_generator,
                    steps_per_epoch=train_generator.samples // BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=validation_generator,
                    validation_steps=validation_generator.samples // BATCH_SIZE)

# Evaluate model on test data
test_loss, test_acc = model.evaluate(test_generator, steps=test_generator.samples // BATCH_SIZE)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_acc)

import matplotlib.pyplot as plt

# Get training and validation accuracy and loss from history
train_accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']
train_loss = history.history['loss']
val_loss = history.history['val_loss']

# Plot accuracy
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(range(1, EPOCHS + 1), train_accuracy, label='Training Accuracy')
plt.plot(range(1, EPOCHS + 1), val_accuracy, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# Plot loss
plt.subplot(1, 2, 2)
plt.plot(range(1, EPOCHS + 1), train_loss, label='Training Loss')
plt.plot(range(1, EPOCHS + 1), val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()


