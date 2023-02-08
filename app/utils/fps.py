from time import time
import cv2

class FPS:
    def __init__(self):
        self.curr_time = time()

    def get_fps(self):
        curr_fps = round((1/(0.000001+time()-self.curr_time)),1)
        self.curr_time = time()
        return curr_fps

    def print_fps(self):
        print(f"FPS: {self.get_fps()}")


    def add_fps_to_image(self,img,fps):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        textLocation           = (30,40)
        fontScale              = 1
        fontColor              = (255,255,255)
        thickness              = 3
        lineType               = 2

        cv2.putText(img,"FPS: "+str(fps), 
                textLocation,
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)