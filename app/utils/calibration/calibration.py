import itertools
import os
from ctypes import *
from dataclasses import dataclass

import cv2

from .threaded_video_capture import ThreadedVideoCapture

confirm_img_text_1 = "Is this the image from the correct webcam? If it is, press 'y' to continue."
confirm_img_text_2 = "If it is not, especially if a black screen is shown, press 'n'."


def _add_confirm_text_to_image(img):
    img_copy = img.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    textLocation1 = (50, 50)
    textLocation2 = (50, 100)
    fontScale = 0.8
    fontColor = (255, 0, 0)
    thickness = 3
    lineType = 2

    cv2.putText(img_copy, confirm_img_text_1,
                textLocation1,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    cv2.putText(img_copy, confirm_img_text_2,
                textLocation2,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    return img_copy


class Calibration:
    def __init__(self, settings_access, display_capture):
        self.data_folder = settings_access.assets_path + "calibration/grey_code_photos/grey_code"
        self.display_capture = display_capture
        self.cam_port = settings_access.read_general_settings("camera_nr")
        self.calib_dll = cdll.LoadLibrary(settings_access.assets_path + "calibration/dlls/ProjectionCalibration.dll")
        self.primary_bounding_box = self.display_capture.get_primary_bounding_box()
        self.projector_bounding_box = self.display_capture.get_projector_bounding_box()
        instruction_image_names = ["place_webcam.jpg", "camera_select.jpg", "grey_code_capture.jpg",
                                   "software_calibration.jpg", "calibration_complete.jpg"]
        self.instruction_images = [
            self.display_capture.frame_primary_resize(cv2.imread(settings_access.assets_path
                                                                 + "calibration/instructions/" + img_name))
            for img_name in instruction_image_names]

    def capture(self):
        """
        Capture gray code pattern frames
        """
        # Setup displays and start camera
        camera = ThreadedVideoCapture(self.cam_port)
        tv_monitor = Monitor("Instructions",
                             (self.primary_bounding_box["left"], self.primary_bounding_box["top"]),
                             (self.primary_bounding_box["width"], self.primary_bounding_box["height"]))
        tv_monitor.open_fullscreen()

        projector_monitor = Monitor("Projector",
                                    (self.projector_bounding_box["left"], self.projector_bounding_box["top"]),
                                    (self.projector_bounding_box["width"], self.projector_bounding_box["height"]))

        # Show first instruction slide
        tv_monitor.display_image(self.instruction_images[0])
        while cv2.waitKey(1) != 32:
            pass

        room_img = camera.read()
        tv_monitor.display_image(self.display_capture.frame_primary_resize(_add_confirm_text_to_image(room_img)))

        while True:
            key = cv2.waitKey(1)
            if key == ord('y'):
                break
            if key == ord('n'):
                camera.close()
                tv_monitor.display_image(self.instruction_images[1])
                while cv2.waitKey(1) != 32:
                    pass
                cv2.destroyAllWindows()
                exit()

        tv_monitor.display_image(self.instruction_images[2])

        gcp = cv2.structured_light.GrayCodePattern.create(self.projector_bounding_box['width'],
                                                          self.projector_bounding_box['height'])
        captured_frames = []

        projector_monitor.open_fullscreen()
        black_projection, white_projection = gcp.getImagesForShadowMasks((self.projector_bounding_box['width'],
                                                                          self.projector_bounding_box['height']),
                                                                         (self.projector_bounding_box['width'],
                                                                          self.projector_bounding_box['height']))
        projector_monitor.display_image(black_projection)
        for projection in itertools.chain(gcp.generate()[1], [black_projection, white_projection]):
            projector_monitor.display_image(projection)
            cv2.waitKey(300)
            captured_frames.append(camera.read())

        projector_monitor.close()
        camera.close()

        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        fs = cv2.FileStorage(os.path.join(self.data_folder, "projection_size.ext"), cv2.FILE_STORAGE_WRITE)
        fs.write("h", self.projector_bounding_box['height'])
        fs.write("w", self.projector_bounding_box['width'])
        fs.release()
        for i, pattern_image in enumerate(captured_frames[:-2]):
            path = os.path.join(self.data_folder, "pattern" + str(i) + ".png")
            cv2.imwrite(path, pattern_image)
        cv2.imwrite(os.path.join(self.data_folder, "blackFrame.png"), captured_frames[-2])
        cv2.imwrite(os.path.join(self.data_folder, "whiteFrame.png"), captured_frames[-1])

        tv_monitor.display_image(self.instruction_images[3])
        self.calibrate()
        tv_monitor.display_image(self.instruction_images[4])
        while cv2.waitKey(1) != 32:
            pass
        tv_monitor.close()
        cv2.destroyAllWindows()

    def calibrate(self):
        """
        Run the calibration script on this classes data folder
        """
        r = cv2.selectROI("Select the TV", cv2.imread(os.path.join(self.data_folder, "blackFrame.png")))
        cv2.destroyWindow("Select the TV")
        contour = (c_int * 8)(r[0], r[1], r[0] + r[2], r[1], r[0] + r[2], r[1] + r[3], r[0], r[1] + r[3])
        self.calib_dll.calibrate(self.data_folder.encode(), contour)

    def read_maps(self):
        """
        Get remap maps from the data folder
        :return:
        """
        fs = cv2.FileStorage(os.path.join(self.data_folder, "map.ext"), cv2.FILE_STORAGE_READ)
        map1 = fs.getNode("map1").mat()
        map2 = fs.getNode("map2").mat()
        fs.release()
        return map1, map2


@dataclass
class Monitor:
    name: str
    position: tuple[int, int]
    resolution: tuple[int, int]

    def open_fullscreen(self):
        """
        Open a fullscreen window on the monitor
        """
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.name, self.position[0], self.position[1])
        cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def display_image(self, img):
        """
        Display given image on the monitor
        :param img: Image to display
        """
        cv2.imshow(self.name, img)

    def close(self):
        """
        Destroy the opencv window
        """
        cv2.destroyWindow(self.name)
