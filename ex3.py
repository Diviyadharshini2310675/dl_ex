import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.utils import get_file
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay
from PIL import Image
import os

# 1. Load pre-trained CNN
model = ResNet50(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

# 2. ImageNet images
urls = [
    "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg"
]

# 3. Class labels
labels = [0, 1, 0, 1, 0, 1]

# 4. Load and preprocess images
X = []

for url in urls:
    file = get_file(os.path.basename(url), url)

    img = Image.open(file).resize((224, 224))
    img = preprocess_input(np.array(img))

    X.append(img)

X = np.array(X)

# 5. Extract high-level features
X = model.predict(X)

print("Feature vector:", X.shape)

# 6. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    labels,
    test_size=0.33,
    random_state=42,
    stratify=labels
)

# 7. New classification layer
clf = LogisticRegression(max_iter=1000)

# 8. Train classifier
clf.fit(X_train, y_train)

# 9. Test classifier
y_pred = clf.predict(X_test)

# 10. Calculate metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, zero_division=0))
print("Recall:", recall_score(y_test, y_pred, zero_division=0))
print("F1-score:", f1_score(y_test, y_pred, zero_division=0))

# 11. Confusion matrix
cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix:")
print(cm)

ConfusionMatrixDisplay(cm).plot()
plt.show()