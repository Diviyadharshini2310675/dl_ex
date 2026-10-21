import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.utils import image_dataset_from_directory
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# 1. Dataset path

DATASET = "imagenette-160"

selected_classes = [
    "n01440764",
    "n02102040",
    "n03028079",
    "n03445777",
    "n03888257"
]

# 2. Load training dataset

train_dataset = image_dataset_from_directory(
    os.path.join(DATASET, "train"),
    class_names=selected_classes,
    image_size=(224, 224),
    batch_size=10,
    shuffle=False
)

# 3. Load testing dataset

test_dataset = image_dataset_from_directory(
    os.path.join(DATASET, "val"),
    class_names=selected_classes,
    image_size=(224, 224),
    batch_size=10,
    shuffle=False
)

print("Dataset Loaded")

# 4. Load pretrained VGG16 without classification layer

model = VGG16(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

print("VGG16 Feature Extractor Loaded")

# 5. Extract feature vectors

def extract_features(dataset):

    features = []
    labels = []

    for images, batch_labels in dataset:

        images = preprocess_input(
            images.numpy().astype(np.float32)
        )

        output = model.predict(images, verbose=0)

        features.extend(output)
        labels.extend(batch_labels.numpy())

    return np.array(features), np.array(labels)


X_train, y_train = extract_features(train_dataset)
X_test, y_test = extract_features(test_dataset)

print("Training Feature Shape:", X_train.shape)
print("Testing Feature Shape:", X_test.shape)
print("Feature Vector Dimension:", X_train.shape[1])

# 6. Train new classification layer

classifier = LogisticRegression(max_iter=1000)

classifier.fit(X_train, y_train)

print("Classifier Trained")

# 7. Predict unseen test images

y_pred = classifier.predict(X_test)

# 8. Calculate performance metrics

print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("Precision:", precision_score(
    y_test, y_pred, average="macro", zero_division=0
))

print("Recall:", recall_score(
    y_test, y_pred, average="macro", zero_division=0
))

print("F1 Score:", f1_score(
    y_test, y_pred, average="macro", zero_division=0
))

# 9. Confusion matrix

cm = confusion_matrix(
    y_test, y_pred,
    labels=np.arange(len(selected_classes))
)

print("\nConfusion Matrix:")
print(cm)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=selected_classes
)

disp.plot(xticks_rotation=45)
plt.title("VGG16 Transfer Learning - Confusion Matrix")
plt.tight_layout()
plt.show()

print("\nExperiment Completed")