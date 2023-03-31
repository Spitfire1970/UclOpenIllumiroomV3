from keras.models import load_model
import cv2
import numpy as np
import os

"""
This module contains a weather detection class that uses a pre-trained neural network model
to predict the weather from an input image frame. The weather classes that can be predicted
are: cloudy, lightning, rain, snow, sandstorm, sunrise.

Attributes:
    model (keras.models.Model): The pre-trained Keras neural network model used for prediction.

Methods:
    __init__(self, model_path): Initializes the weather detection class by loading the pre-train model from the specified model_path.
    predict_weather(self, frame): Predicts the weather class from an input image frame. The input image must have 3 channels and be of size 64x64. 
    Returns the predicted weather class as a string.
"""
class weatherdetection:
    def __init__(self, model_path):
        self.model = load_model(os.path.join(model_path, "neural_network"))

    def predict_weather(self, frame):
        """
        Predicts the weather class from an input image frame.

        Args:
            frame (numpy.ndarray): The input image frame. Must have 3 channels and be of size 64x64.

        Returns:
            str: The predicted weather class as a string. Possible values are: 'cloudy', 'lightning', 'rain','snow', 'sandstorm', or 'sunrise'.
        """
        # weather_img = cv2.imread(str(image_path))
        frame = np.flip(frame[:,:,:3],2)
        img_array = cv2.resize(frame, (64,64))
        img_array = (img_array/255).astype(np.float32)

        print(np.min(img_array), np.max(img_array))
        img_array = np.expand_dims(img_array, axis=0)
        predictions = self.model.predict(img_array)
        predicted_class_index = np.argmax(predictions)

        if predicted_class_index == 0:
            print("cloudy")
            return "cloudy"
        elif predicted_class_index == 1:
            print("lightning")
            return "lightning"
        elif predicted_class_index == 2:
            print("rain")
            return "rain"
        elif predicted_class_index == 3:
            print("snow")
            return "snow"
        elif predicted_class_index == 4:
            print("sandstorm")
            return "sandstorm"
        elif predicted_class_index == 5:
            print("snow")
            return "snow"
        else:
            print("sunrise")
            return "sunrise"
        
