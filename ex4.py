import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding
from tensorflow.keras.utils import get_file
from PIL import Image

# 1. CNN encoder
cnn = ResNet50(weights="imagenet", include_top=False, pooling="avg")

# 2. Images and captions
urls = [
    "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg",
    "https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg"
]

captions = [
    "a photo of a sunflower",
    "a photo of a person"
]

# 3. Extract CNN features
X = []

for url in urls:
    file = get_file(url.split("/")[-1], url)
    img = Image.open(file).resize((224,224))
    img = preprocess_input(np.array(img))
    X.append(img)

X = cnn.predict(np.array(X))

# 4. Add START and END
captions = ["start " + c + " end" for c in captions]

# 5. Tokenize
tok = Tokenizer()
tok.fit_on_texts(captions)

seq = tok.texts_to_sequences(captions)
seq = pad_sequences(seq, padding="post")

vocab = len(tok.word_index) + 1

# 6. Input and output
decoder_in = seq[:, :-1]
decoder_out = seq[:, 1:]

# 7. LSTM decoder
image = Input(shape=(2048,))
text = Input(shape=(decoder_in.shape[1],))

img = Dense(128, activation="relu")(image)
img = tf.keras.layers.RepeatVector(decoder_in.shape[1])(img)

word = Embedding(vocab, 128)(text)

x = tf.keras.layers.Concatenate()([img, word])
x = LSTM(128, return_sequences=True)(x)
output = Dense(vocab, activation="softmax")(x)

model = Model([image, text], output)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy"
)

# 8. Train
model.fit(
    [X, decoder_in],
    np.expand_dims(decoder_out, -1),
    epochs=10
)

print("Model trained!")
print("Vocabulary:", tok.word_index)

def generate_caption(feature):
    
    text = [tok.word_index["start"]]

    for i in range(8):

        s = pad_sequences(
            [text],
            maxlen=decoder_in.shape[1],
            padding="post"
        )

        p = model.predict([feature, s], verbose=0)

        word = np.argmax(p[0, len(text)-1])

        if word == 0:
            break

        w = tok.index_word[word]

        if w == "end":
            break

        text.append(word)

    return " ".join(tok.index_word[i] for i in text[1:])

print("Generated caption:", generate_caption(X[0:1]))