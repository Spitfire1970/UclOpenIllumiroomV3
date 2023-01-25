from .mode import Mode
from utils.sound_analysis import SoundDetector

# TODO: refactor generate_frames method
# - single responsibility principle!!

class Wobble(Mode):
    # TODO: remove center_x, center_y, start, 
    # and end by getting these values from 
    # .settings/mode_settings.json
    def __init__(
            self, img, center_x, center_y, start, 
            end, threshold, main_window
        ):
        self.img = img
        self.num_frames = 15
        self.center_x, self.center_y = center_x, center_y
        self.start, self.end = start, end
        self.sound_detector = SoundDetector(threshold)
        self.threshold = threshold
        self.frames = []
        self.main_window = main_window

    def generate_frames(self):
        self.frames = []
        for i in range(self.num_frames):
            amplitude = 15 * (i/self.num_frames)
            frequency = 0.12 * (i/self.num_frames)
            # Interpolation factor
            factor = 1 - i / self.num_frames

            # Create a mask to exclude pixels inside the TV rectangle
            mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            cv2.rectangle(mask, self.start, self.end, (255, 255, 255), -1)

            # Calculate distance from the center of the effect
            distance = np.sqrt((self.x - self.center_x) ** 2 + (self.y - self.center_y) ** 2)
            distance[self.mask == 255] = 0
            fractal_noise = np.random.normal(0, self.fractal_amplitude, distance.shape)
            distance = distance + fractal_noise

            # Calculate the angle of the pixel
            angle = distance * frequency

            # Calculate the new x and y coordinates using the sine wave equation
            new_x = self.x + amplitude * np.sin(angle)
            new_y = self.y + amplitude * np.cos(angle)

            # Interpolate between new pixel pos and the original pos
            # (to bring animation to stop how it started)
            new_x = np.float32(self.original_x * (1 - factor) + new_x * factor)
            new_y = np.float32(self.original_y * (1 - factor) + new_y * factor)

            # Use remap with new coords and Lanczos Interpolation method
            output_img = cv2.remap(self.img, new_x, new_y, cv2.INTER_LANCZOS4)
            self.frames.append(output_img)


    def trigger(self):
        self.generate_frames()
        while True:
            if self.sound_detector.detect_loud_sound() > self.threshold:
                for frame in self.frames:
                    height, width, channel = frame.shape
                    bytesPerLine = 3 * width
                    qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
                    self.main_window.label.setPixmap(QtGui.QPixmap(qImg))
                    self.main_window.update()
                    time.sleep(0.05)
            else:
                height, width, channel = self.img.shape
                bytesPerLine = 3 * width
                qImg = QtGui.QImage(self.img, width, height, bytesPerLine, QtGui.QImage.Format.Format_RGB888).rgbSwapped()
                self.main_window.label.setPixmap(QtGui.QPixmap(self.img))
                self.main_window.update()
