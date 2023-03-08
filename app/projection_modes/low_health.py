from .mode import Mode
from cv2 import TERM_CRITERIA_EPS, TERM_CRITERIA_MAX_ITER, KMEANS_RANDOM_CENTERS, kmeans, cvtColor, COLOR_BGR2GRAY, medianBlur, adaptiveThreshold, ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, COLOR_GRAY2BGR, addWeighted
import numpy as np
from pathlib import Path

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
        #print(self.num_low_health_frames)
        self.low_health_frames = self.generate_low_health_frames()

        self.number_clusters = 1
        self.criteria = (TERM_CRITERIA_EPS + TERM_CRITERIA_MAX_ITER, 10, 1.0)
        self.flags = KMEANS_RANDOM_CENTERS

        self.previous_avgBG = None
        self.start_low_health = 1.2
        self.end_low_health = 2.5
        self.range = self.end_low_health - self.start_low_health
        self.scaling_factor = self.num_low_health_frames/self.range
    
        
    def kmeans_get_colour(self, data):
        #number of colors
        _, _, colour_list = kmeans(data, self.number_clusters, None, self.criteria, 10, self.flags)
        return colour_list[0]

    def crop_and_resize_image_to_data(self,frame):
        height, width, _ = np.shape(frame)
        x_left = 0
        x_right = int(width*7/8)
        w = int(width/8)

        y = int(height/8)
        h = int(height*6/8)
        sct_left = frame[y:y+h, x_left:x_left+w]
        sct_right = frame[y:y+h, x_right:x_right+w]

        #reshape and concatenate data from images
        height, width, _ = np.shape(sct_left)
        data_left = np.reshape(sct_left, (height * width, 4))
        data_left = np.float32(data_left) 

        height, width, _ = np.shape(sct_right)
        data_right = np.reshape(sct_left, (height * width, 4))
        data_right = np.float32(data_right) 

        data = np.concatenate((data_left,data_right))
        return data

    def scale_low_health_to_frames(self, colour):

        b, g, r, a = colour
        avgBG = (b+g+1)/2
        #print("colour is: ",colour)
        #print("red/avg :",r/avgBG)
        frame_num = 0
        # if (r+1) / avgBG > 3:
        #     frame_num = self.num_low_health_frames
        # elif (r+1) / avgBG > 2.4:
        #     frame_num = int(self.num_low_health_frames*3/4)
        # elif (r+1) / avgBG > 1.8:
        #     frame_num = int(self.num_low_health_frames*1/2)
        # elif (r+1) / avgBG >= 1.45:
        #     frame_num = int(self.num_low_health_frames*1/4)

        #In Bo2, anything below 1.2 is no blood, maximum of 2.5
        #Scale from 1.2, to 2.5 use linear scale for frame num
        #THerefore subtract 1.2 from each colour reading, then scale from 
        #0 to 1.3

        avgRBG = (r+1) / avgBG

        avgRBG_scaled = (avgRBG - self.start_low_health) * self.scaling_factor
        frame_num = int(avgRBG_scaled)

        if frame_num > self.num_low_health_frames:
            frame_num = self.num_low_health_frames - 1
        elif frame_num < 0:
            frame_num = 0
        #print("framenum:",frame_num)
        return frame_num
    
    def generate_low_health_frames(self):
        gray = cvtColor(self.background_img, COLOR_BGR2GRAY)
        
        gray = medianBlur(gray, 5)
        
        # Detect edges in image, create colour image
        edges = adaptiveThreshold(
                    gray, 255, ADAPTIVE_THRESH_MEAN_C, 
                    THRESH_BINARY,11, 7
                )
        
        colour_edges = cvtColor(edges, COLOR_GRAY2BGR)       
        colour_edges[np.where((colour_edges == [0,0,0]).all(axis = 2))] = [0, 0, 0] #BGR - Colour of lines
        colour_edges[np.where((colour_edges == [255,255,255]).all(axis = 2))] = [0, 0, 200] #BGR - colour of background

        #Generate specified number of frames, first with 0 change in colour, get red until almost fully red
        generated_frames = []
        print("Generating Low Health Frames")
        for opacity in range(0,self.num_low_health_frames,1):
            opacity_background = round(1-opacity/self.num_low_health_frames,2)
            opacity_edges= round(opacity/self.num_low_health_frames,2)
            generated_frames.append(addWeighted(self.background_img, opacity_background, colour_edges, opacity_edges, -5))
        return generated_frames


    def trigger(self):
        #Display capture 
        input_frame = self.display_capture.capture_frame()
        frames = [input_frame]

        data = self.crop_and_resize_image_to_data(input_frame)
        
        kmeans_colour = self.kmeans_get_colour(data)

        low_health_frame_num = self.scale_low_health_to_frames(kmeans_colour)
        if self.num_low_health_frames-low_health_frame_num > 0.8 * self.num_low_health_frames:
            frames = [self.low_health_frames[low_health_frame_num]] 
        else:
            frames = [self.low_health_frames[low_health_frame_num]] * (3)
        print("colour: ",kmeans_colour)
        print("frame num: ",low_health_frame_num)
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