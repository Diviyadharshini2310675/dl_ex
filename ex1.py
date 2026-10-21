import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input,decode_predictions
from tensorflow.keras.utils import image_dataset_from_directory

DATASET="imagenette-160"

selected_classes=[
    "n01440764",   # tench
    "n02102040",   # English springer
    "n03028079",   # church
    "n03445777",   # golf ball
    "n03888257"
]


train_path=os.path.join(
    DATASET,
    "train"
)

train_dataset=image_dataset_from_directory(
    train_path,
    labels="inferred",
    class_names=selected_classes,
    image_size=(224,224),
    batch_size=10,
    shuffle=True
)

val_path=os.path.join(
    DATASET,
    "val"
)

val_dataset=image_dataset_from_directory(
    val_path,
    labels="inferred",
    class_names=selected_classes,
    image_size=(224,224),
    batch_size=10,
    shuffle=True
)

print("Selected Class")
print(selected_classes)


model=VGG16(
    weights="imagenet",
    include_top=True
)
print("model Loaded")

images , labels=next(
    iter(val_dataset)
)

print("Images")
print(images.shape)

plt.figure(figsize=(112,8))

for i in range(min(10,len(images))):

    plt.subplot(2,5,i+1)

    plt.imshow(
        images[i].numpy().astype("uint8")
    )

    plt.title(
        selected_classes[labels[i]]
    )

    plt.axis("off")

plt.tight_layout()
plt.show()


x=images.numpy().astype(np.float32)

x=preprocess_input(x)

print("Preprocessed image")
print(x.shape)

pred=model.predict(x)

for i in range(len(pred)):
    print("Images",i+1)

    print("Original labels:",selected_classes[labels[i]])

    top5=decode_predictions(
        pred[i:i+1],
        top=5
    )[0]

    for _,name,probability in top5:
        print(
            f"{name}",
            f"{probability*100:.2f}%"
        )


feature_model=tf.keras.Model(
    inputs=model.input,
    outputs=model.get_layer(
        "block3_conv3"
    ).output
)

features=feature_model.predict(x)

print("Input Shape:",x.shape)
print("Intermediate representation:",features.shape)
print("Output shape:",pred.shape)

plt.figure(figsize=(6, 6))

plt.imshow(
    features[0, :, :, 0],
    cmap="gray"
)

plt.title(
    "Intermediate Representation - Block3 Conv3"
)

plt.axis("off")

plt.show()