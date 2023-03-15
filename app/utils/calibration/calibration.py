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
    def __init__(self, settings_access, display_capture):
        print("Calibration init")
        self.data_folder = settings_access.assets_path + "calibration/grey_code_photos/grey_code/"
        self.exe_path = settings_access.assets_path + "calibration/exe/CalibrationExecutable.exe"
        self.room_image_path = settings_access.assets_path + "room_image/"
        self.display_capture = display_capture
        self.settings_access = settings_access
        self.cam_port = settings_access.read_general_settings("camera_nr")
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
        print("Starting webcam")
        camera = ThreadedVideoCapture(self.cam_port)
        # camera = cv2.VideoCapture(self.cam_port, cv2.CAP_DSHOW)
        tv_monitor = Monitor("Instructions",
                             (self.primary_bounding_box["left"], self.primary_bounding_box["top"]),
                             (self.primary_bounding_box["width"], self.primary_bounding_box["height"]))
        tv_monitor.open_fullscreen()

        # Show first instruction slide
        tv_monitor.display_image(self.instruction_images[0])
        while cv2.waitKey(1) != 32:
            pass

        test_img = camera.read()
        camera.close()
        tv_monitor.display_image(self.display_capture.frame_primary_resize(self.add_confirm_text_to_image(test_img)))

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

        tv_monitor.display_image(self.instruction_images[2])
        cv2.waitKey(100)

        subprocess.run([self.exe_path,
                        "capture",
                        self.data_folder,
                        str(self.cam_port),
                        str(self.projector_bounding_box["left"]),
                        str(self.projector_bounding_box["top"])], capture_output=False)

        tv_monitor.display_image(self.instruction_images[3])

        self.calibrate()

        # Take extra image for room image (maximum resolution),
        # locate projection and TV areas

        tv_monitor.display_image(self.instruction_images[4])
        while cv2.waitKey(1) != 32:
            pass
        tv_monitor.close()
        cv2.destroyAllWindows()

    def calibrate(self):
        """
        Run the calibration script on this classes data folder
        """

        r = self.select_projection_area_and_tv(Monitor("Projector",
                                                       (self.primary_bounding_box["left"],
                                                        self.primary_bounding_box["top"]),
                                                       (self.primary_bounding_box["width"],
                                                        self.primary_bounding_box["height"])))
        pnt1 = (int(r[0] - (r[2] / 2)), int(r[1] - (r[3] / 2)))
        pnt2 = (int(r[0] + (3 * r[2] / 2)), int(r[1] + (3 * r[3] / 2)))
        exe_data = [self.exe_path,
                    "calibrate",
                    self.data_folder] + \
                   [str(pnt) for pnt in [pnt1[0], pnt1[1], pnt2[0], pnt1[1], pnt2[0], pnt2[1], pnt1[0], pnt2[1]]]
        subprocess.run(exe_data, capture_output=False)

    def select_projection_area_and_tv(self, monitor):
        room_image_camera = cv2.VideoCapture(self.cam_port, cv2.CAP_DSHOW)
        room_image_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        room_image_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        monitor.open_fullscreen()
        self.take_picture_background(monitor)
        cv2.waitKey(2000)
        result, projection_area = room_image_camera.read()
        monitor.close()

        # img = projection_area
        projection_area_roi = self.add_text_to_image(projection_area.copy(),
                                                     "Select the 4 corners of the projection area, then press 'Space'. Right click to reselect.")
        img_height, img_width, _ = projection_area_roi.shape
        img = cv2.resize(projection_area_roi, (img_width // 2, img_height // 2))  # double-check resizing
        corners = self.get_projection_corners(img=img)
        corners = self.order_corners(crns=corners)
        transformed_proj_roi = self.perspective_transform(img, corners)
        # Resize the image to projector resolution
        transformed_proj_roi = self.display_capture.resize_image_fit_projector_each_frame(transformed_proj_roi)

        # projection_area_roi = self.add_text_to_image(projection_area.copy(), "Please draw a box around the projection area, then press 'space'")
        # area = cv2.selectROI("Select Projection Area", projection_area_roi)
        # cv2.destroyAllWindows()
        # projection_area = projection_area[int(area[1]):int(area[1]+area[3]), int(area[0]):int(area[0]+area[2])]
        # cv2.imwrite(self.room_image_path+"room_img.jpg", projection_area)

        tv_area = transformed_proj_roi.copy()
        tv_area_roi = self.add_text_to_image(tv_area.copy(),
                                             "Please draw a box around the TV, then press 'Space'")
        area = cv2.selectROI("Select TV", tv_area_roi)
        cv2.destroyAllWindows()
        tv_area[int(area[1]):int(area[1] + area[3]), int(area[0]):int(area[0] + area[2])] = 0

        # tv_area = self.display_capture.resize_image_fit_projector_each_frame(tv_area)
        cv2.imwrite(self.room_image_path + "room_img_noTV.jpg", tv_area)

        self.save_tv_coords(area)
        return area

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

    def add_text_to_image(self, img, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        textLocation1 = (50, 50)
        fontScale = 0.8
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

        cv2.imshow("Select Projection Area", img)
        while len(data['points']) != max_points:
            print("Please select all 4 corners to proceed.")
            # Set callback function for any mouse event
            cv2.setMouseCallback("Select Projection Area", self.mouse_handler, data)
            cv2.waitKey(0)
            cv2.setMouseCallback("Select Projection Area", lambda *args: None)
        cv2.destroyWindow("Select Projection Area")

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
        return result

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
