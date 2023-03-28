import os
from ctypes import *
from dataclasses import dataclass
import subprocess

import cv2
import numpy as np
from scipy.spatial import distance as dist

from .threaded_video_capture import ThreadedVideoCapture

confirm_img_text_1 = "Is this the image from the correct webcam? If it is, press 'y' to continue."
confirm_img_text_2 = "If it is not, especially if a black screen is shown, press 'n'."


class Calibration:
    """
    Calibration class is used to walk the user through a calibration process,
    It shows step-by-step instructions and executes an external executable file
    to capture and store GrayCode Patterns as well as run calibration algorithm on them.
    """
    def __init__(self, settings_access, display_capture):
        print("Calibration init")
        self.data_folder = os.path.join(settings_access.assets_path, "calibration\\grey_code_photos\\grey_code\\")
        self.exe_path = os.path.join(settings_access.assets_path, "calibration\\exe\\CalibrationExecutable.exe")
        self.room_image_path = os.path.join(settings_access.assets_path, "room_image/")
        self.display_capture = display_capture
        self.settings_access = settings_access
        self.calibration_state = settings_access.read_general_settings("calibration_state")
        self.cam_port = settings_access.read_general_settings("camera_nr")
        self.primary_bounding_box = self.display_capture.get_primary_bounding_box()
        self.projector_bounding_box = self.display_capture.get_projector_bounding_box()
        instruction_image_names = ["place_webcam.jpg", "camera_select.jpg", "grey_code_capture.jpg",
                                   "software_calibration.jpg", "calibration_complete.jpg", "calibration_unsuccessful.jpg"]
        self.instruction_images = [
            self.display_capture.frame_primary_resize(cv2.imread(settings_access.assets_path
                                                                 + "calibration/instructions/" + img_name))
            for img_name in instruction_image_names]


    def hardware_setup(self, tv_monitor):
        # Show first instruction - webcam, projector setup
        tv_monitor.display_image(self.instruction_images[0])
        while cv2.waitKey(1) != 32:
            pass

        # Start camera
        print("Starting webcam")
        camera = ThreadedVideoCapture(self.cam_port)

        # Verify if correct camera has been chosen in MFC
        test_img = camera.read()
        camera.close()
        resized_image = self.display_capture.frame_primary_resize(test_img)
        confirm_camera_image = self.add_confirm_text_to_image(resized_image)
        tv_monitor.display_image(confirm_camera_image)

        while True:
            key = cv2.waitKey(1)
            if key == ord('y'):
                break
            if key == ord('n'):
                tv_monitor.display_image(self.instruction_images[1])
                while cv2.waitKey(1) != 32:
                    pass
                cv2.destroyAllWindows()
                exit()
        
        # Capture projected gray code pattern frames
        tv_monitor.display_image(self.instruction_images[2])
        cv2.waitKey(100)
        self.capture()


    def software_setup(self, tv_monitor):
        tv_monitor.display_image(self.instruction_images[3])

        if self.select_projection_area_and_tv(Monitor("Projector",
                (self.projector_bounding_box["left"],
                self.projector_bounding_box["top"]),
                (self.projector_bounding_box["width"],
                self.projector_bounding_box["height"]))
            ):
            if self.calibrate():
                # Calibration complete
                tv_monitor.display_image(self.instruction_images[4])
                self.calibration_state = "hardware"
            else:
                # Calibration unsuccessful - try again
                tv_monitor.display_image(self.instruction_images[5])
                self.calibration_state = "software"
        else:
            # Calibration unsuccessful - try again
            tv_monitor.display_image(self.instruction_images[5])
            self.calibration_state = "software"

        while cv2.waitKey(1) != 32:
            pass
        tv_monitor.close()
        cv2.destroyAllWindows()


    def setup_system(self):
        """
        """
        tv_monitor = Monitor("Instructions",
                             (self.primary_bounding_box["left"], self.primary_bounding_box["top"]),
                             (self.primary_bounding_box["width"], self.primary_bounding_box["height"]))
        tv_monitor.open_fullscreen()

        # Store the state of the calibration so that the
        # user doesn't have to re-do gray code capture etc.
        # when they perform an invalid input for software calibration
        if self.calibration_state == "hardware":
            self.hardware_setup(tv_monitor)
            self.calibration_state = "software"
        if self.calibration_state == "software":
            self.software_setup(tv_monitor)
        
        general_settings_json = self.settings_access.read_settings("general_settings.json")
        general_settings_json["calibration_state"] = self.calibration_state
        self.settings_access.write_settings("general_settings.json", general_settings_json)


    def capture(self):
        """
        Capture gray code pattern frames
        """
        subprocess.run([self.exe_path,
                        "capture",
                        self.data_folder,
                        str(self.cam_port),
                        "640",
                        "360",
                        str(self.projector_bounding_box["left"]),
                        str(self.projector_bounding_box["top"])], capture_output=False)


    def calibrate(self):
        """
        Run the calibration script on this classes data folder
        """
        win_name = "Select Adjusted Display Contour"
        r = cv2.selectROI(win_name, self.add_text_to_image(cv2.imread(os.path.join(self.data_folder, "blackFrame.png")),
                                                                                    "Select desired projection area."))
        # Check if ROI has been selected and if selection is cancelled
        if cv2.waitKey(1) == ord('c') or r == (0, 0, 0, 0):
            cv2.destroyWindow(win_name)
            return False
        cv2.destroyWindow(win_name)

        contour = (r[0], r[1], r[0] + r[2], r[1], r[0] + r[2], r[1] + r[3], r[0], r[1] + r[3])
        exe_data = [self.exe_path,
                    "calibrate",
                    self.data_folder,
                    str(self.projector_bounding_box["width"]),
                    str(self.projector_bounding_box["height"])] + \
                   [str(i) for i in contour] + ["2", "7"]
        subprocess.run(exe_data, capture_output=False)
        return True


    def select_projection_area_and_tv(self, monitor):
        room_image_camera = cv2.VideoCapture(self.cam_port, cv2.CAP_DSHOW)
        room_image_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        room_image_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        monitor.open_fullscreen()
        self.take_picture_background(monitor)
        cv2.waitKey(1000)
        result, projection_area = room_image_camera.read()
        cv2.waitKey(1000)
        result, projection_area = room_image_camera.read()
        cv2.waitKey(1000)
        monitor.close()

        # Select projection area
        projection_area_roi = self.add_text_to_image(projection_area.copy(),
                                "Select the 4 corners of the projection area, then "
                                + "press 'Space'. Right click to reselect.")
        img_height, img_width, _ = projection_area_roi.shape
        img = cv2.resize(projection_area_roi, (img_width // 2, img_height // 2))
        corners = self.get_projection_corners(img=img)
        if corners is not None:
            corners = self.order_corners(crns=corners)
            homography, transformed_proj_roi = self.perspective_transform(img, corners)
            # Resize the image to projector resolution
            transformed_proj_roi = self.display_capture.resize_image_fit_projector_each_frame(transformed_proj_roi)

            # Select TV area
            self.select_tv_area(transformed_proj_roi)
            return True
        return False


    def select_tv_area(self, projector_roi):
        tv_area = projector_roi.copy()
        tv_area_roi = self.add_text_to_image(tv_area.copy(),
                        "Please draw a box around the TV, then press 'Space'. "
                        + "Press 'c' to cancel selection.")

        cv2.imshow("Select TV", tv_area_roi)
        area = cv2.selectROI("Select TV", tv_area_roi)
        # Check if TV has been selected before exiting window
        # or if selection has been cancelled
        if cv2.waitKey(1) == ord('c') or area == (0, 0, 0, 0):
            cv2.destroyWindow("Select TV")
            return False
        cv2.destroyWindow("Select TV")

        # Set TV area to be black
        tv_area[int(area[1]):int(area[1] + area[3]), int(area[0]):int(area[0] + area[2])] = 0
        cv2.imwrite(self.room_image_path + "room_img_noTV.jpg", tv_area)

        self.save_tv_coords(area)


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

    def add_confirm_text_to_image(self, img):
        img_copy = img.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        textLocation1 = (50, 50)
        textLocation2 = (50, 100)
        fontScale = 1.2
        fontColor = (255, 255, 0)
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

    def add_text_to_image(self, img, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        textLocation1 = (50, 50)
        fontScale = 1.2
        fontColor = (255, 255, 0)
        thickness = 3
        lineType = 2

        cv2.putText(img, text,
                    textLocation1,
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

        return img

    def take_picture_background(self, monitor):
        height = self.projector_bounding_box['height']
        width = self.projector_bounding_box['width']
        image = np.zeros((height, width, 3), np.uint8)

        rgb_color = (74, 78, 84)
        colour = tuple(reversed(rgb_color))
        image[:] = colour

        monitor.display_image(image)

    def mouse_handler(self, event, x, y, flags, data):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(data['points']) < data['max_points']:
                cv2.circle(data['img'], (x, y), 2, (0, 255, 255), -1)
                cv2.circle(data['img'], (x, y), 12, (0, 255, 255), 2)
                cv2.imshow("Select Projection Area", data['img'])
                data['points'].append([x, y])

        if event == cv2.EVENT_RBUTTONDOWN:
            data['img'] = data['original_img'].copy()
            cv2.imshow("Select Projection Area", data['img'])
            data['points'] = []

    def get_projection_corners(self, img):
        # Set up data to send to mouse handler
        max_points = 4
        data = {}
        data['original_img'] = img
        data['img'] = img.copy()
        data['points'] = []
        data['max_points'] = max_points

        try:
            cv2.imshow("Select Projection Area", img)
            while ((len(data['points']) != max_points)):
                # key = cv2.waitKey(1)
                if cv2.getWindowProperty("Select Projection Area", cv2.WND_PROP_VISIBLE) < 1:
                    print("WINDOW CLOSED")
                    # cv2.destroyAllWindows()
                    break
                else:
                    print("Please select all 4 corners to proceed.")
                    # Set callback function for any mouse event
                    cv2.setMouseCallback("Select Projection Area", self.mouse_handler, data)
                    cv2.waitKey(0)
                    cv2.setMouseCallback("Select Projection Area", lambda *args: None)
            cv2.destroyWindow("Select Projection Area")
        except cv2.error as e:
            # For when the user Xs the window
            if "NULL window: 'Select Projection Area'" in str(e):
                return None


        # Convert array to np.array
        points = np.array(data['points'], dtype="float32")
        return points

    def order_corners(self, crns):
        # Sort corners by ascending x-value
        x_sorted = crns[np.argsort(crns[:, 0]), :]
        left_most = x_sorted[:2, :]
        right_most = x_sorted[2:, :]

        # Sort leftmost corners by ascending y-value
        left_most = left_most[np.argsort(left_most[:, 1]), :]
        # Top left, bottom left
        (tl, bl) = left_most

        # Calc distance between top-left corner and the rightmost ones
        D = dist.cdist(tl[np.newaxis], right_most, "euclidean")[0]
        # Bottom right, top right
        (br, tr) = right_most[np.argsort(D)[::-1], :]
        return np.array([tl, tr, br, bl], dtype="float32")

    def perspective_transform(self, img, crns_from):
        height, width = 1080 // 2, 1920 // 2
        crns_to = np.array([[0, 0], [width, 0], [width, height], [0, height]], np.float32)

        matrix = cv2.getPerspectiveTransform(crns_from, crns_to)
        result = cv2.warpPerspective(img, matrix, (width, height))

        # cv2.imshow('View of Projection Area', result)
        # cv2.waitKey(0)
        # cv2.destroyWindow("View of Projection Area")
        return matrix, result

    def update_mode_settings(self, settings, new_data):
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")

        for i in range(len(settings)):
            mode_settings_json["wobble"]["tv_data"][settings[i]] = new_data[i]

        self.settings_access.write_settings("mode_settings.json", mode_settings_json)

    def save_tv_coords(self, tv_area_roi):
        top_left = [tv_area_roi[0], tv_area_roi[1]]
        bottom_right = [tv_area_roi[0] + tv_area_roi[2], tv_area_roi[1] + tv_area_roi[3]]

        # Calculate the center of the TV
        center_x = int((top_left[0] + bottom_right[0]) / 2)
        center_y = int((top_left[1] + bottom_right[1]) / 2)

        settings = ["tv_top_left", "tv_bottom_right", "tv_center_x", "tv_center_y"]
        new_values = [top_left, bottom_right, center_x, center_y]

        # Save TV coords for modes which apply a mask where the TV is
        self.update_mode_settings(settings, new_values)


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
