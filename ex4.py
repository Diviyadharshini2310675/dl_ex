import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, RepeatVector
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# 1. Load dataset

DATASET = "imagenette-160"

selected_classes = [
    "n01440764",
    "n02102040",
    "n03028079",
    "n03445777",
    "n03888257"
]

dataset = image_dataset_from_directory(
    os.path.join(DATASET, "train"),
    class_names=selected_classes,
    image_size=(224, 224),
    batch_size=10,
    shuffle=True
)

# 2. Load pretrained CNN encoder

cnn = VGG16(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

print("VGG16 Encoder Loaded")

# 3. Get images and labels

images, labels = next(iter(dataset))

plt.imshow(images[0].numpy().astype("uint8"))
plt.title(selected_classes[int(labels[0].numpy())])
plt.axis("off")
plt.show()

# 4. Extract image features

x = preprocess_input(
    images.numpy().astype(np.float32)
)

features = cnn.predict(x, verbose=0)

print("Feature Shape:", features.shape)

# 5. Convert class labels into captions

class_names = [
    "tench",
    "English springer",
    "church",
    "golf ball",
    "parachute"
]

captions = [
    "startseq a photo of a " + class_names[int(label)] + " endseq"
    for label in labels.numpy()
]

  print("Example Caption:", captions[0])

# 6. Tokenize captions

tokenizer = Tokenizer(
    filters="",
    lower=True
)

tokenizer.fit_on_texts(captions)

sequences = tokenizer.texts_to_sequences(captions)

vocab_size = len(tokenizer.word_index) + 1
max_length = max(len(seq) for seq in sequences)

sequences = pad_sequences(
    sequences,
    maxlen=max_length,
    padding="post"
)

print("Vocabulary Size:", vocab_size)
print("Caption Sequence Shape:", sequences.shape)

# 7. Prepare next-word training sequences

X_img = []
X_seq = []
y_word = []

for i, seq in enumerate(sequences):

    for j in range(1, len(seq)):

        X_img.append(features[i])
        X_seq.append(
            pad_sequences(
                [seq[:j]],
                maxlen=max_length - 1,
                padding="post"
            )[0]
        )
        y_word.append(seq[j])

X_img = np.array(X_img)
X_seq = np.array(X_seq)
y_word = np.array(y_word)

# 8. Build LSTM decoder

image_input = Input(shape=(512,))
image_features = Dense(128, activation="relu")(image_input)
image_features = RepeatVector(max_length - 1)(image_features)

text_input = Input(shape=(max_length - 1,))
text_features = Embedding(
    vocab_size,
    128,
    mask_zero=True
)(text_input)

merged = tf.keras.layers.Concatenate()(
    [image_features, text_features]
)

lstm_output = LSTM(128)(merged)
output = Dense(vocab_size, activation="softmax")(lstm_output)

model = Model(
    inputs=[image_input, text_input],
    outputs=output
)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# 9. Train caption decoder

model.fit(
    [X_img, X_seq],
    y_word,
    epochs=30,
    verbose=1
)

print("CNN-LSTM Model Trained")

# 10. Generate caption for an image

def generate_caption(feature):

    caption = ["startseq"]

    for _ in range(max_length):

        seq = tokenizer.texts_to_sequences(
            [" ".join(caption)]
        )

        seq = pad_sequences(
            seq,
            maxlen=max_length - 1,
            padding="post"
        )

        prediction = model.predict(
            [feature.reshape(1, 512), seq],
            verbose=0
        )

        word_id = np.argmax(prediction[0])

        word = tokenizer.index_word.get(word_id, "")

        if word == "endseq" or word == "":
            break

        caption.append(word)

    return " ".join(
        word for word in caption
        if word != "startseq"
    )


# 11. Display generated caption

index = 0

generated = generate_caption(features[index])

print("\nExpected Caption:")
print(captions[index])

print("\nGenerated Caption:")
print(generated)

plt.imshow(images[index].numpy().astype("uint8"))
plt.title("Generated: " + generated)
plt.axis("off")
plt.show()

print("\nExperiment Completed")