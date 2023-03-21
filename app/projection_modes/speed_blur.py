from .mode import Mode

import numpy as np
import cv2
from screeninfo import get_monitors
from time import time, sleep

# import the necessary packages for tesseract OCR
import pytesseract

class SpeedBlur(Mode):

    """
    A class for applying a speed blur effect to a captured display from a racing game, such as Forza Horizon 4.

    Key Attributes:
        display_capture: An instance of the `DisplayCapture` class.
        speedometer_box_ratios: A dictionary containing the ratios for the speedometer bounding box.
        
        primary_bounding_box: A dictionary containing the primary bounding box values.
        speedometer_bounding_box: A dictionary containing the values for the speedometer bounding box.

        tesseract_config: The configuration settings for the tesseract OCR.
        median_speeds_queue: A list containing the most recent speed values.

        current_blur: The current blur value.
        blur_division_factor: The division factor for the blur value.
        show_blur_amount: A boolean indicating whether or not to show the blur amount.

    Methods:
        trigger(): Captures a frame and applies the speed blur effect.
        apply_mode_to_frame(frame, blur_amount): Applies the speed blur effect to a given frame.
        get_speedometer_bounding_box(): Returns a dictionary containing the values for the speedometer bounding box.
        speedometer_cut_out(frame): Cuts out the speedometer area from a given frame.
        get_blur_amount(frame_speedometer): Gets the blur amount based on the speed value.
        preprocess_speed(img): Preprocesses the given image to be used for OCR.
        get_speed(tesseract_config, image): Returns the speed value obtained from OCR.
        add_median_speed(new_speed): Adds a new speed value to the median speeds queue.
        get_median_speed(): Returns the median speed value from the median speeds queue.
        add_speed_to_image(img, speed): Adds the speed value text to the given image.
    """

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
        """
        Once triggered, screen record a frame, apply the blurring, then return the frame.
        Returns:
            list of numpy.ndarray: List containing the single appropriately blurred frame.
        """

        frames = [None]
        frame = self.display_capture.capture_frame()
        
        frame_speedometer = self.speedometer_cut_out(frame)
        blur_amount = self.get_blur_amount(frame_speedometer)
        frames[0] = self.apply_mode_to_frame(frame, blur_amount)
        return frames
    

    def apply_mode_to_frame(self,frame, blur_amount):
        """
        Apply blurring to the input frame using the specified blur_amount.
        Parameters:
            frame (numpy.ndarray): Input frame to be blurred.
            blur_amount (int): Amount of blurring to be applied to the frame.
        Returns:
            numpy.ndarray: Blurred frame.
        """

        frame = cv2.blur(frame, (blur_amount, blur_amount) ,0)

        if self.show_blur_amount:
            self.add_speed_to_image(frame, str(blur_amount))
        return frame



    def get_speedometer_bounding_box(self):
        """
        Get the bounding box coordinates for the speedometer area in the primary display bounding box.
        Returns:
            dict: Dictionary containing the top, left, width, and height of the speedometer bounding box.
        """
     
        top_prim = self.primary_bounding_box['top']
        left_prim = self.primary_bounding_box['left']

        #Ratio of how much of screen wish to be taken in bounding box

        bounding_box_speedometer = {'top':top_prim + int(self.primary_bounding_box['height']*(self.speedometer_square_top_ratio)), 'left': left_prim + int(self.primary_bounding_box['width']*self.speedometer_square_left_ratio), 'width': int(self.primary_bounding_box['width']*self.speedometer_width_ratio), 'height': int(self.primary_bounding_box['height']*self.speedometer_height_ratio)}
        return bounding_box_speedometer

    
    def speedometer_cut_out(self,frame):
        """
        Extract the speedometer region from the input frame using the bounding box coordinates.
        Parameters:
            frame (numpy.ndarray): Input frame to extract the speedometer region from.
        Returns:
            numpy.ndarray: Cropped speedometer region from the input frame.
        """
        
        top = self.speedometer_bounding_box["top"]
        left = self.speedometer_bounding_box["left"]
        width = self.speedometer_bounding_box["width"]
        height = self.speedometer_bounding_box["height"]
        return frame[top:top+height, left:left+width]
    

    
    def get_blur_amount(self, frame_speedometer):
        """
        Get the blur amount to be applied to the frame using the speedometer region.
        Parameters:
            frame_speedometer (numpy.ndarray): Cropped speedometer region from the input frame.
        Returns:
            int: Amount of blurring to be applied to the frame.
        """
        
        speed = self.get_speed(self.tesseract_config, frame_speedometer)
        return speed


    def preprocess_speed(self,img):
        """
        Preprocess the input image by removing the Alpha channel and inverting its color.
        Args:
            img (numpy.ndarray): Input image to be preprocessed.
        Returns:
            numpy.ndarray: Preprocessed image.
        """
               
        img = 255 - img
        
        return img

    def get_speed(self,tesseract_config,image):
        """
        Get the speed from the input image using Tesseract OCR.
        Args:
            tesseract_config (str): Tesseract configuration settings.
            image (numpy.ndarray): Input image to extract the speed from.
        Returns:
            int: The median speed extracted from the 5 previous input images
        """
        
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
        """
        Add a new speed value to the median speeds queue and remove the oldest value.
        Args:
            new_speed (int): New speed value to be added to the queue.
        """
        self.median_speeds_queue.pop(0)
        self.median_speeds_queue.append(new_speed)

    def get_median_speed(self):
        """
        Get the median speed from the median speeds queue.
        Returns:
            int: The median speed value.
        """
        median_sort = self.median_speeds_queue.copy()
        median_sort.sort()
        return median_sort[2]

    
    def add_speed_to_image(self, img, speed):
        """
        Add the speed value text to the input image.
        Args:
            img (numpy.ndarray): Input image to add the speed to.
            speed (str): Speed value to be added to the input image.
        """
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