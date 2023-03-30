#Deprecated class, should be removed in the future
from cv2 import (rectangle, imshow, namedWindow, setMouseCallback,
waitKey, destroyAllWindows, EVENT_LBUTTONDOWN, EVENT_LBUTTONUP
)

MODE = "wobble"

class TVDetection():
    def __init__(self, image, settings_access) -> None:
        self.img = image
        self.top_left = None
        self.bottom_right = None
        self.settings_access = settings_access
    
    def update_mode_settings(self, settings, new_data):
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")

        for i in range(len(settings)):
            mode_settings_json[MODE][settings[i]] = new_data[i]
        
        self.settings_access.write_settings("mode_settings.json", mode_settings_json)
        # return mode_settings_json[mode][setting]


    def on_mouse(self, event, x, y, flags, params):
        # Allow user to create a boundary box for the TV
        if event == EVENT_LBUTTONDOWN:
            self.top_left = (x, y)
        elif event == EVENT_LBUTTONUP:
            self.bottom_right = (x, y)
            rectangle(self.img, self.top_left, self.bottom_right, (0, 255, 0), 2)
            imshow("Detect TV", self.img)

    def calc_center(self):
        # Calculate the center of the TV
        center_x = int((self.top_left[0] + self.bottom_right[0]) / 2)
        center_y = int((self.top_left[1] + self.bottom_right[1]) / 2)
        # TODO: handle exceptions

        settings = ["tv_top_left", "tv_bottom_right", "tv_center_x", "tv_center_y"]
        new_values = [self.top_left, self.bottom_right, center_x, center_y]

        self.update_mode_settings(settings, new_values)
        # return center_x, center_y

    def detect_tv(self):
        namedWindow("Detect TV")
        setMouseCallback("Detect TV", self.on_mouse)
        #add text on the selection window with instructions, since console will not be visible
        
        while True:
            imshow("Detect TV", self.img)
            key = waitKey(1)
            if key == ord("q") and self.top_left is not None:
                break
            elif key == ord("q") and self.top_left is None:
                print("Please select your primary monitor before exiting!")
                pass
        destroyAllWindows()
        for i in range (1,5):
            waitKey(1)

        self.calc_center()
        return self.img
