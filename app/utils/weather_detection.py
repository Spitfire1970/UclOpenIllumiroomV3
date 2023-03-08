from keras.models import load_model
from cv2 import resize
import numpy as np
import os

class weatherdetection:
    def __init__(self, model_path):
        self.model = load_model(os.path.join(model_path, "neural_network"))

    def predict_weather(self, frame):
        # weather_img = imread(str(image_path))
        frame = np.flip(frame[:,:,:3],2)
        img_array = resize(frame, (64,64))
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
        
