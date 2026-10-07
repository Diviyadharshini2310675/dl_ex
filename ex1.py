import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.utils import get_file
from PIL import Image
import os

# 1. Load pretrained VGG16
print("Loading VGG16 model...")
model = VGG16(weights="imagenet")

# 2. Image URLs
urls = [
    "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg"
]

images = []

# 3. Load and preprocess images
for url in urls:
    file = get_file(os.path.basename(url), url)

    img = Image.open(file).convert("RGB")
    img = img.resize((224, 224))

    x = np.array(img, dtype=np.float32)
    x = preprocess_input(x)

    images.append(x)

# Convert list to NumPy array
x = np.array(images)

# 4. Display images
plt.figure(figsize=(8, 4))

for i in range(len(images)):
    plt.subplot(1, len(images), i + 1)

    # Convert image for display
    display_img = (x[i] - x[i].min()) / (x[i].max() - x[i].min())

    plt.imshow(display_img)
    plt.axis("off")
    plt.title(f"Image {i + 1}")

plt.tight_layout()
plt.show()

# 5. Predict
print("\nPredicting images...")
pred = model.predict(x)

# 6. Top-5 predictions
for i in range(len(pred)):

    print("\nImage", i + 1)

    # IMPORTANT:
    # Use pred[i:i+1] instead of pred[i]
    predictions = decode_predictions(pred[i:i + 1], top=5)[0]

    for label, name, prob in predictions:
        print(f"{name}: {prob * 100:.2f}%")

# 7. Intermediate representation

layer_model = tf.keras.Model(
    inputs=model.input,
    outputs=model.get_layer("block3_conv3").output
)

features = layer_model.predict(x)

print("\nInput shape:", x.shape)
print("Intermediate representation:", features.shape)
print("Output shape:", pred.shape)

# 8. Display feature map
plt.figure(figsize=(6, 6))

plt.imshow(features[0, :, :, 0], cmap="gray")

plt.title("Intermediate Representation - Block3 Conv3")
plt.axis("off")

plt.show()