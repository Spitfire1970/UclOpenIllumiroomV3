# import cv2
# Note: window displayed using cv2.imshow, TODO: change this


class TVDetection():
    def __init__(self, start, end, image) -> None:
        self.start = start
        self.end = end
        self.img = image

    def on_mouse(self, event, x, y, flags, params):
        # Allow user to create a boundary box for the TV
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.end = (x, y)
            cv2.rectangle(self.img, self.start, self.end, (0, 255, 0), 2)
            cv2.imshow("Detect TV", self.img)

    def calc_center(self):
        # Calculate the center of the TV
        center_x = int((self.start[0] + self.end[0]) / 2)
        center_y = int((self.start[1] + self.end[1]) / 2)
        # TODO: handle exceptions
        f = open("TV_info.txt", "w")
        f.write(f"{center_x}  {center_y}  {self.start}  {self.end}")
        f.close()
        return center_x, center_y, self.start, self.end

    def detect_tv(self):
        cv2.namedWindow("Detect TV")
        cv2.setMouseCallback("Detect TV", self.on_mouse)
        while True:
            cv2.imshow("Detect TV", self.img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        return self.calc_center()
