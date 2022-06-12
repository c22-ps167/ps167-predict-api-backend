import os

import numpy as np
import tensorflow as tf
from flask import Flask, request
from tensorflow import keras
from werkzeug.utils import secure_filename

from model.repository import list_item

model = keras.models.load_model('model/model.h5')


def do_predict(path):
    image_size = (100, 100)

    img = keras.preprocessing.image.load_img(
        path, target_size=image_size
    )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    image = np.vstack([img_array])
    predictions = model.predict(image, batch_size=10)
    score = predictions[0]

    result = ""
    for index in range(len(score)):
        if score[index] == 1:
            result = list_item[index]

    result_dict = {
        "data": result
    }
    return result_dict


# FLASK

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def hello_world():
    return "<p>ps167</p>"


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "<p>No file part!</p>"
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return "<p>No selected file!</p>"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        result = do_predict(UPLOAD_FOLDER + "/" + filename)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return result
