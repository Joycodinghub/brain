from flask import Flask, request, render_template
import os
import cv2
from PIL import Image
import numpy as np
from keras.models import load_model

app = Flask(__name__)

# Load the trained model
model = load_model("myModel.keras")

# Define a function to preprocess images
def preprocess_image(image):
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64, 64))
    image = np.array(image)
    image = image / 255.0
    return image

@app.route('/', methods=['GET', 'POST'])
def classify_image():
    if request.method == 'POST':
        # Get the uploaded image
        uploaded_image = request.files['image']

        if uploaded_image:
            try:
                # Save the uploaded image to the "uploads" folder
                upload_path = os.path.join('uploads', uploaded_image.filename)
                uploaded_image.save(upload_path)

                # Read and preprocess the uploaded image
                image = cv2.imread(upload_path)
                image = preprocess_image(image)

                # Make a prediction using the loaded model
                prediction = model.predict(np.expand_dims(image, axis=0))

                # Determine the result based on the prediction
                result = "Tumor Detected" if prediction > 0.5 else "No Tumor Detected"
                # print("prediction:"+prediction)
                surety = int(prediction[0][0] * 100)
                if(result=="Tumor Detected"):
                    return render_template('result.html', result=result, surety="Surety :"+ str(surety) +"%",prediction=prediction)
                else:
                    return render_template('result.html', result=result,prediction=prediction)

            except Exception as e:
                return f'Error processing image: {str(e)}'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'image' in request.files:
#         image = request.files['image']
#         if image.filename != '':
#             # Specify the path to the folder where you want to save the image
#             upload_path = 'uploads/' + image.filename
#             image.save(upload_path)  # Save the image to the specified folder
#             return 'Image uploaded successfully!'
#     return 'Image upload failed.'

# if __name__ == '__main__':
#     app.run(debug=True)
