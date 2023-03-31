from time import time
from cv2 import putText, FONT_HERSHEY_SIMPLEX


class FPS:
    """
    FPS is a class used for calculating and displaying current frames per second
    """
    def __init__(self):
        self.curr_time = time()

    def get_fps(self):
        """
        Calculate fps from last call
        :return: current fps count
        """
        # Calculate the current fps
        curr_fps = round((1 / (0.000001 + time() - self.curr_time)), 1)
        self.curr_time = time()
        return curr_fps

    def print_fps(self):
        """
        Print fps to the console
        """
        print(f"FPS: {self.get_fps()}")

    def add_fps_to_image(self, img, fps):
        """
        Add fps count text to an image
        :param img: Image to display fps on
        :param fps: Fps value
        """
        font = FONT_HERSHEY_SIMPLEX
        textLocation = (30, 40)
        fontScale = 1
        fontColor = (255, 255, 255)
        thickness = 3
        lineType = 2

        # Receive an image and add the FPS count in the corner
        putText(img, "FPS: " + str(fps),
                textLocation,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)
