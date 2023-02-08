from .mode import Mode
import cv2
import numpy as np
from pathlib import Path
import time

class LowHealth(Mode):
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture=None
        ):
        self.settings_access = settings_access
        self.background_img = background_img
        self.display_capture = display_capture
        self.num_low_health_frames = settings_access.read_mode_settings("low_health","num_low_health_frames")
        print(self.num_low_health_frames)
        self.low_health_frames = self.generate_low_health_frames()

        self.number_clusters = 1
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        self.flags = cv2.KMEANS_RANDOM_CENTERS
    
        
    def kmeans_get_colour(self, data):
        #number of colors
        compactness, labels, colour = cv2.kmeans(data, self.number_clusters, None, self.criteria, 10, self.flags)
        return colour

    def crop_and_resize_image_to_data(self,frame):
        height, width, _ = np.shape(frame)
        x_left = 0
        x_right = int(width*7/8)
        w = int(width/8)

        y = int(height/8)
        h = int(height*6/8)
        left_img = frame[y:y+h, x_left:x_left+w]
        right_img = frame[y:y+h, x_right:x_right+w]

        img = cv2.hconcat([left_img,right_img])
        height, width, _ = np.shape(img)
        data = np.reshape(img, (height * width, 4))
        data = np.float32(img) 
        return data

    def scale_low_health_to_frames(self, colour):

        b, g, r, a = colour
        avgBG = (b+g+1)/2
        print("colour is: ",colour)
        print("red/avg :",r/avgBG)
        if (r+1) / avgBG > 3:
            return 4
        elif (r+1) / avgBG > 2.4:
            return 3
        elif (r+1) / avgBG > 1.8:
            return 2
        elif (r+1) / avgBG >= 1.45:
            return 1
        else:
            return 0 # Black background
    
    def generate_low_health_frames(self):
        gray = cv2.cvtColor(self.background_img, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.medianBlur(gray, 5)
        
        # Detect edges in image, create colour image
        edges = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                    cv2.THRESH_BINARY,11, 7
                )
        
        colour_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)       
        colour_edges[np.where((colour_edges == [0,0,0]).all(axis = 2))] = [0, 0, 255] #BGR
        colour_edges[np.where((colour_edges == [255,255,255]).all(axis = 2))] = [30, 30, 200] #BGR

        #Generate specified number of frames, first with 0 change in colour, get red until almost fully red
        generated_frames = []
        print("Generating Low Health Frames")
        for opacity in range(0,self.num_low_health_frames,1):
            opacity_background = round(1-opacity/self.num_low_health_frames,2)
            opacity_edges= round(opacity/self.num_low_health_frames,2)
            generated_frames.append(cv2.addWeighted(self.background_img, opacity_background, colour_edges, opacity_edges, -10))
        return generated_frames


    def trigger(self):
        #Display capture 
        input_frame = self.display_capture.capture_frame()
        frames = [input_frame]
        data = self.crop_and_resize_image_to_data(input_frame)
        kmeans_colour = self.kmeans_get_colour(data)
        print(kmeans_colour[10])
        #low_health_frame_num = self.scale_low_health_to_frames(kmeans_colour)
        
        #frames = [self.low_health_frames[low_health_frame_num]]
        return frames
    """
    def trigger(self):
        # Save image
        # cartoon_img_name = (__file__[:__file__.index("app") 
        #     + len("app")]+"/assets/generated/cartoon_view.jpeg")
        #All images are stored in the assets folder
        low_health_img_name = self.settings_access.get_image_path("generated/low_health_red_lines_view.jpeg")
        low_health_img = Path(low_health_img_name)
        if low_health_img.is_file():
            self.img = cv2.imread(low_health_img_name)
        else: 
            self.generate_low_health_images()
            cv2.imwrite(low_health_img_name, self.img)

        frames = [self.img]
        return frames
    """