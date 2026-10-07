import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.utils import get_file
from PIL import Image

# 1. Load CNN
model = ResNet50(weights="imagenet")

# 2. Load image
url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
file = get_file("image.jpg", url)

img = Image.open(file).resize((224,224))
x = preprocess_input(np.array(img))
x = np.expand_dims(x, 0)

# 3. Select CNN layers
layers = [
    "conv1_conv",
    "conv2_block3_out",
    "conv4_block6_out"
]

# 4. Extract feature maps
outputs = [model.get_layer(l).output for l in layers]
fm = tf.keras.Model(model.input, outputs).predict(x)

# 5. Display feature maps
for name, f in zip(layers, fm):

    print(name, ":", f.shape)

    plt.figure(figsize=(8,4))

    for i in range(6):
        plt.subplot(2,3,i+1)
        plt.imshow(f[0,:,:,i], cmap="gray")
        plt.axis("off")

    plt.suptitle(name)
    plt.show()

# 6. Compare feature maps
print("\nComparison:")
print("Early        : Edges and simple textures")
print("Intermediate : Patterns, shapes and textures")
print("Deep         : Complex and high-level features")

# 7. Display learned filters
filters = model.get_layer("conv1_conv").get_weights()[0]

plt.figure(figsize=(8,4))

for i in range(6):
    plt.subplot(2,3,i+1)
    plt.imshow(filters[:,:,0,i], cmap="gray")
    plt.axis("off")

plt.suptitle("Convolution Filters")
plt.show()