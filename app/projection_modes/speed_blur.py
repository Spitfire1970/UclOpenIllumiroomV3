from .mode import Mode

import numpy as np
import cv2
from PIL import Image
from screeninfo import get_monitors
from time import time, sleep

# import the necessary packages for tesseract OCR
import pytesseract

class SpeedBlur(Mode):
    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            audio_capture=None
        ):
        self.display_capture = display_capture

        self.speedometer_box_ratios = settings_access.read_mode_settings_object("speed_blur","speedometer_box_ratios")
        self.speedometer_square_left_ratio = self.speedometer_box_ratios["square_left_ratio"]
        self.speedometer_square_top_ratio = self.speedometer_box_ratios["square_top_ratio"]
        self.speedometer_width_ratio = self.speedometer_box_ratios["width_ratio"]
        self.speedometer_height_ratio = self.speedometer_box_ratios["height_ratio"]

        self.primary_bounding_box = display_capture.get_primary_bounding_box()
        self.speedometer_bounding_box =  self.get_speedometer_bounding_box()

        self.tesseract_config = r'--oem 3 --psm 8'
        self.median_speeds_queue = [1,1,1,1,1]

        self.current_blur = 1
        self.blur_division_factor = settings_access.read_mode_settings("speed_blur", "blur_division_factor")
        self.show_blur_amount = settings_access.read_mode_settings("speed_blur", "show_blur_amount")

    def trigger(self):
        #Once triggered, screen record a frame, apply the blurring, then return the frame
        
        frames = [None]
        #frame= self.display_capture.capture_frame_projector_resize()
        frame = self.display_capture.capture_frame()
        
        frame_speedometer = self.speedometer_cut_out(frame)
        blur_amount = self.get_blur_amount(frame_speedometer)
        frames[0] = self.apply_mode_to_frame(frame, blur_amount)
        return frames
    

    def apply_mode_to_frame(self,frame, blur_amount):

        frame = cv2.blur(frame, (blur_amount, blur_amount) ,0)

        if self.show_blur_amount:
            self.add_speed_to_image(frame, str(blur_amount))
        return frame



    def get_speedometer_bounding_box(self):
     
        top_prim = self.primary_bounding_box['top']
        left_prim = self.primary_bounding_box['left']

        #Ratio of how much of screen wish to be taken in bounding box

        bounding_box_speedometer = {'top':top_prim + int(self.primary_bounding_box['height']*(self.speedometer_square_top_ratio)), 'left': left_prim + int(self.primary_bounding_box['width']*self.speedometer_square_left_ratio), 'width': int(self.primary_bounding_box['width']*self.speedometer_width_ratio), 'height': int(self.primary_bounding_box['height']*self.speedometer_height_ratio)}
        return bounding_box_speedometer

    
    def speedometer_cut_out(self,frame):
        top = self.speedometer_bounding_box["top"]
        left = self.speedometer_bounding_box["left"]
        width = self.speedometer_bounding_box["width"]
        height = self.speedometer_bounding_box["height"]
        return frame[top:top+height, left:left+width]
    

    
    def get_blur_amount(self, frame_speedometer):

        
        speed = self.get_speed(self.tesseract_config, frame_speedometer)
        return speed


    def preprocess_speed(self,img):
        #inverse image colour
               
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        img = 255 - img
        
        return img

    def get_speed(self,tesseract_config,image):
        
        prep_proc = self.preprocess_speed(image)
        #cv2.imshow("speed", prep_proc)
        #cv2.imshow("name",prep_proc)
        speed=""
        speed_raw = pytesseract.image_to_string(prep_proc, config = tesseract_config)
        speed=speed.join(filter(str.isdigit, speed_raw))

        try:
            speed = int(speed)//self.blur_division_factor

            if speed > 0:
                self.add_median_speed(speed)     
        except:
            pass

        return self.get_median_speed()
    
    def add_median_speed(self, new_speed):
        self.median_speeds_queue.pop(0)
        self.median_speeds_queue.append(new_speed)

    def get_median_speed(self):
        median_sort = self.median_speeds_queue.copy()
        median_sort.sort()
        return median_sort[2]

    
    def add_speed_to_image(self, img, speed):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        textLocation           = (30,100)
        fontScale              = 0.8
        fontColor              = (255,0,0,255)
        thickness              = 3
        lineType               = 2

        cv2.putText(img,"SPEED: "+speed, 
                textLocation,
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)