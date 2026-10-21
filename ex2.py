import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.utils import image_dataset_from_directory


# ============================================================
# 1. DATASET PATH
# ============================================================

DATASET = "imagenette-160"

selected_classes = [
    "n01440764",   # tench
    "n02102040",   # English springer
    "n03028079",   # church
    "n03445777",   # golf ball
    "n03888257"    # parachute
]
  

# ============================================================
# 2. LOAD DATASET
# ============================================================

val_path = os.path.join(DATASET, "val")

val_dataset = image_dataset_from_directory(
    val_path,
    labels="inferred",
    class_names=selected_classes,
    image_size=(224, 224),
    batch_size=5,
    shuffle=True
)

print("Selected Classes:")
print(selected_classes)


# ============================================================
# 3. LOAD PRE-TRAINED VGG16
# ============================================================

model = VGG16(
    weights="imagenet",
    include_top=True
)

print("VGG16 Model Loaded")


# ============================================================
# 4. GET ONE IMAGE
# ============================================================

images, labels = next(iter(val_dataset))

image = images[0:1].numpy().astype(np.float32)

print("Input Shape:", image.shape)


# ============================================================
# 5. DISPLAY ORIGINAL IMAGE
# ============================================================

plt.figure(figsize=(5, 5))

plt.imshow(images[0].numpy().astype("uint8"))

plt.title(
    "Original Image: " +
    selected_classes[int(labels[0].numpy())]
)

plt.axis("off")
plt.show()


# ============================================================
# 6. PREPROCESS IMAGE
# ============================================================

x = preprocess_input(image)

print("Preprocessed Image Shape:", x.shape)


# ============================================================
# 7. SELECT THREE CONVOLUTIONAL LAYERS
# ============================================================

layer_names = [
    "block1_conv1",   # Shallow layer
    "block3_conv3",   # Intermediate layer
    "block5_conv3"    # Deep layer
]

feature_model = tf.keras.Model(
    inputs=model.input,
    outputs=[
        model.get_layer(name).output
        for name in layer_names
    ]
)


# ============================================================
# 8. EXTRACT FEATURE MAPS
# ============================================================

features = feature_model.predict(x)

for name, feature in zip(layer_names, features):

    print("\nLayer:", name)
    print("Feature Map Shape:", feature.shape)


# ============================================================
# 9. VISUALIZE FEATURE MAPS
# ============================================================

for name, feature in zip(layer_names, features):

    plt.figure(figsize=(12, 6))

    plt.suptitle(
        "Feature Maps - " + name
    )

    for i in range(8):

        plt.subplot(2, 4, i + 1)

        plt.imshow(
            feature[0, :, :, i],
            cmap="viridis"
        )

        plt.title("Channel " + str(i + 1))
        plt.axis("off")

    plt.tight_layout()
    plt.show()


# ============================================================
# 10. VISUALIZE LEARNED CONVOLUTIONAL FILTERS
# ============================================================

filter_layer = model.get_layer("block1_conv1")

filters, biases = filter_layer.get_weights()

print("\nFilter Layer:", filter_layer.name)
print("Filter Shape:", filters.shape)

# VGG16 first convolution has 64 filters of size 3 x 3 x 3

plt.figure(figsize=(10, 10))

for i in range(16):

    f = filters[:, :, :, i]

    # Normalize filter values for display
    f_min = f.min()
    f_max = f.max()

    f = (f - f_min) / (f_max - f_min + 1e-8)

    plt.subplot(4, 4, i + 1)

    plt.imshow(f)
    plt.title("Filter " + str(i + 1))
    plt.axis("off")

plt.suptitle("Learned Filters - block1_conv1")
plt.tight_layout()
plt.show()


# ============================================================
# 11. COMPARE FEATURE MAP DIMENSIONS
# ============================================================

print("\n========== DIMENSION COMPARISON ==========")

for name, feature in zip(layer_names, features):

    print(
        name,
        "->",
        feature.shape
    )

print("\nExperiment Completed")