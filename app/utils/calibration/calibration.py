import itertools
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
    to capture and store Gray-Code Patterns as well as run calibration algorithm on them.
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
                                   "software_calibration.jpg", "calibration_complete.jpg",
                                   "calibration_unsuccessful.jpg"]
        self.instruction_images = [
            self.display_capture.frame_primary_resize(cv2.imread(settings_access.assets_path
                                                                 + "calibration/instructions/" + img_name))
            for img_name in instruction_image_names]

    def capture(self, projection_size: tuple[int, int], camera: ThreadedVideoCapture, projector):
        """
        Capture gray code pattern frames using provided camera and projector
        :param projection_size: Size of the projection
        :param camera: Video Capture to use when capturing the images
        :param projector: Monitor representing the projector
        """
        gcp = cv2.structured_light.GrayCodePattern.create(projection_size[0],
                                                          projection_size[1])
        captured_frames = []
        projector.open_fullscreen()
        black_projection, white_projection = gcp.getImagesForShadowMasks(projection_size, projection_size)
        projector.display_image(black_projection)
        for projection in itertools.chain(gcp.generate()[1], [black_projection, white_projection]):
            projector.display_image(projection)
            cv2.waitKey(300)
            captured_frames.append(camera.read())

        projector.close()

        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        fs = cv2.FileStorage(os.path.join(self.data_folder, "projection_size.ext"), cv2.FILE_STORAGE_WRITE)
        fs.write("h", projection_size[1])
        fs.write("w", projection_size[0])
        fs.release()
        for i, pattern_image in enumerate(captured_frames[:-2]):
            path = os.path.join(self.data_folder, "pattern" + str(i) + ".png")
            cv2.imwrite(path, pattern_image)
        cv2.imwrite(os.path.join(self.data_folder, "blackFrame.png"), captured_frames[-2])
        cv2.imwrite(os.path.join(self.data_folder, "whiteFrame.png"), captured_frames[-1])

    def hardware_setup(self, camera, tv_monitor):
        """Displays instructions for webcam and projector setup on the
        TV monitor, starts the webcam camera and verifies if the correct camera
        has been chosen in the MFC settings. Then, it captures the projected 
        gray-code pattern frames.

        Parameters:
        -----------
        tv_monitor : Monitor
            A Monitor object representing the TV monitor to be used for 
            displaying the system setup instructions and for confirming 
            the chosen webcam.

        Returns:
        --------
        None
        """
        # Show first instruction - webcam, projector setup
        tv_monitor.display_image(self.instruction_images[0])
        while cv2.waitKey(1) != 32:
            pass

        # Verify if correct camera has been chosen in MFC
        test_img = camera.read()
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
                camera.close()
                exit()

        # Capture projected gray-code pattern frames
        tv_monitor.display_image(self.instruction_images[2])
        cv2.waitKey(100)
        projector_monitor = Monitor("Projection",
                             (self.projector_bounding_box["left"], self.projector_bounding_box["top"]),
                             (self.projector_bounding_box["width"], self.projector_bounding_box["height"]))
        self.capture((640, 360), camera, projector_monitor)

    def software_setup(self, camera, tv_monitor):
        """Displays instructions for software setup on the TV monitor, 
        opens windows to select the projection area, TV and the final
        projection area. If successful, the projector-camera calibration, 
        using the gray-code patterns, begins. If at any stage, invalid inputs
        have been received, calibration is unsuccessful and the user is
        asked to try again. The calibration state is saved. When unsuccessful,
        the calibration state is set to 'software' to start the setup from the
        software part directly (skipping the gray-code capture etc.).

        Parameters:
        -----------
        tv_monitor : Monitor
            A Monitor object representing the TV monitor to be used for 
            displaying the instructions.

        Returns:
        --------
        None
        """
        tv_monitor.display_image(self.instruction_images[3])

        if self.select_projection_area_and_tv(camera, Monitor("Projector",
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
        # All instructions have been shown 
        # so close monitor
        tv_monitor.close()
        cv2.destroyAllWindows()

    def setup_system(self):
        """Sets up the system by instantiating a Monitor object for 
        the TV to display instructions. Checks whether to start the 
        setup procedure from the hardware or software setup based on the 
        calibration state. After completing calibration, the updated
        calibration state is saved to the system settings.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        tv_monitor = Monitor("Instructions",
                             (self.primary_bounding_box["left"], self.primary_bounding_box["top"]),
                             (self.primary_bounding_box["width"], self.primary_bounding_box["height"]))
        tv_monitor.open_fullscreen()

        camera = ThreadedVideoCapture(self.cam_port)
        if not camera.opened():
            camera.close()
            tv_monitor.display_image(self.instruction_images[1])
            while cv2.waitKey(1) != 32:
                pass
            cv2.destroyAllWindows()
            exit()
        # Store the state of the calibration so that the
        # user doesn't have to re-do gray code capture etc.
        # when they perform an invalid input for software calibration
        if self.calibration_state == "hardware":
            self.hardware_setup(camera, tv_monitor)
            self.calibration_state = "software"
        if self.calibration_state == "software":
            self.software_setup(camera, tv_monitor)

        general_settings_json = self.settings_access.read_settings("general_settings.json")
        general_settings_json["calibration_state"] = self.calibration_state
        self.settings_access.write_settings("general_settings.json", general_settings_json)

    def calibrate(self):
        """Runs the calibration script on this class'
        data folder after selecting the adjusted display contour ROI.

        Parameters:
        -----------
        None

        Returns:
        --------
        bool
            False if ROI is not selected or selection is cancelled, True otherwise.
        """
        win_name = "Select Adjusted Display Contour"
        r = cv2.selectROI(win_name, self.add_text_to_image(cv2.imread(os.path.join(self.data_folder, "blackFrame.png")),
                                                           "Select desired projection area."))
        # Check if ROI has not been selected and if selection is cancelled
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

    def select_projection_area_and_tv(self, camera, monitor):
        """Capture an image of the room while a plain grey frame is 
        projected. Displays an OpenCV window to select the projection area
        in the image. If successfully, selected, displays an OpenCV window to
        select the TV in the image.

        Parameters:
        -----------
        monitor : Monitor
            A Monitor object represeting the projector display for projecting
            a grey frame.

        Returns:
        --------
        bool
            True if the selection process is successful, False otherwise.
        """

        monitor.open_fullscreen()
        self.take_picture_background(monitor)
        cv2.waitKey(1000)
        projection_area = camera.read()
        cv2.waitKey(1000)
        monitor.close()
        cv2.waitKey(1000)
        # release instance of ThreadedVideoCapture
        # as it is no longer required
        camera.close()

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
            if self.select_tv_area(transformed_proj_roi):
                return True
        return False

    def select_tv_area(self, projector_roi):
        """Displays an OpenCV window for selecting the region of 
        the perspective transformed projection area image that 
        corresponds to the TV screen. Save an image with a black
        mask where TV is to assets\\room_image and the coordinates 
        for the TV to the Wobble mode settings (as it's the only mode
        which uses the TV coords presently).

        Parameters:
        -----------
        projector_roi : numpy.ndarray
            The image of the perspective transformed projection area image.

        Returns:
        --------
        bool: True if the TV region was successfully selected, False otherwise.
        
        """
        tv_area = projector_roi.copy()
        tv_area_roi = self.add_text_to_image(tv_area.copy(),
                                             "Please draw a box around the TV, then press 'Space'. "
                                             + "Press 'c' to cancel selection.")

        cv2.imshow("Select TV", tv_area_roi)
        area = cv2.selectROI("Select TV", tv_area_roi)
        # Check if TV has not been selected before exiting window
        # or if selection has been cancelled
        if cv2.waitKey(1) == ord('c') or area == (0, 0, 0, 0):
            cv2.destroyWindow("Select TV")
            return False
        cv2.destroyWindow("Select TV")

        # Set TV area to be black
        tv_area[int(area[1]):int(area[1] + area[3]), int(area[0]):int(area[0] + area[2])] = 0
        cv2.imwrite(self.room_image_path + "room_img_noTV.jpg", tv_area)

        self.save_tv_coords(area)
        return True

    def read_maps(self):
        """
        Get remap maps from the data folder.

        Parameters:
        -----------
        None
        
        Returns:
        --------
        map1, map2 : tuple of numpy.ndarray
            Returns a tuple of two numpy arrays that contain remap maps.
        """
        fs = cv2.FileStorage(os.path.join(self.data_folder, "map.ext"), cv2.FILE_STORAGE_READ)
        map1 = fs.getNode("map1").mat()
        map2 = fs.getNode("map2").mat()
        fs.release()
        return map1, map2

    def add_confirm_text_to_image(self, img):
        # Used when verifying the correct webcam has
        # been chosen
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
        # Used to add text onto an image
        # displayed using an OpenCV window
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
        """Project a grey frame on the projector display.

        Parameters:
        -----------
        monitor : Monitor
            A Monitor object representing the projector display.

        Returns:
        --------
        None
        """
        height = self.projector_bounding_box['height']
        width = self.projector_bounding_box['width']
        image = np.zeros((height, width, 3), np.uint8)

        rgb_color = (74, 78, 84)
        colour = tuple(reversed(rgb_color))
        image[:] = colour

        monitor.display_image(image)

    def mouse_handler(self, event, x, y, flags, data):
        """Handle mouse events for selecting points in an image.
        Points can be selected upto the max number of points. 
        If right click is pressed, remove all the points selected 
        so far and reset the image that's displayed to the original 
        room image.

        Parameters:
        -----------
        event : int
            The event that occurred.
        x : int
            The x-coordinate of the event.
        y : int
            The y-coordinate of the event.
        flags : int
            Any flags that were passed to the event.
        data : dict
            A dictionary containing the original image, image with
            the points selected so far drawn as circles, 
            coordinates of the points and the max points that can
            be selected.

        Returns:
        --------
        None
        
        """
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
        """
        Retrieve the 4 corners of the projection area that
        have been selected on the given image of the room. 

        Parameters:
        -----------
        img : numpy.ndarray
            An array containing the image of the room.

        Returns:
        --------
        numpy.ndarray or None
            An array of four points representing the selected corners,
            or None if the window was closed without selecting four corners.
        """
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
                if cv2.getWindowProperty("Select Projection Area", cv2.WND_PROP_VISIBLE) < 1:
                    break
                else:
                    print("Please select all 4 corners to proceed.")
                    # Set callback function for any mouse event
                    cv2.setMouseCallback("Select Projection Area", self.mouse_handler, data)
                    cv2.waitKey(0)
                    cv2.setMouseCallback("Select Projection Area", lambda *args: None)
            cv2.destroyWindow("Select Projection Area")
        except cv2.error as e:
            # For when the user presses the X on the window
            if "NULL window: 'Select Projection Area'" in str(e):
                return None

        # Convert array to np.array
        points = np.array(data['points'], dtype="float32")
        return points

    def order_corners(self, crns):
        """Orders corners of a quadrilateral in the 
        top-left, top-right, bottom-right, bottom-left order.

        Parameters:
        -----------
        crns : numpy.ndarray
            An array with the corner points of the quadrilateral.

        Returns:
        --------
        numpy.ndarray
            An array with the ordered corner points.
        """
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
        """Performs a perspective transformation on the image of 
        the room based on the given source and destination corners.

        Parameters:
        -----------
        img : numpy.ndarray
            The image to be transformed.
        crns_from : numpy.ndarray
            An array with the initial corner points.

        Returns:
        --------
        matrix, result : tuple of numpy.ndarray
            A tuple with the transformation matrix and the transformed image.
        """
        height, width = 1080 // 2, 1920 // 2
        crns_to = np.array([[0, 0], [width, 0], [width, height], [0, height]], np.float32)

        matrix = cv2.getPerspectiveTransform(crns_from, crns_to)
        result = cv2.warpPerspective(img, matrix, (width, height))

        return matrix, result

    def update_mode_settings(self, settings, new_data):
        """Updates mode settings with the new data about the
        TV coordinates for the Wobble mode (this is the only
        mode which uses this info right now - should save TV coords
        to general settings in the future).

        Parameters:
        -----------
        settings : list
            A list with the names of the settings to be updated.
        new_data : list
            A list with the new data to update the settings.

        Returns:
        --------
        None
        """
        mode_settings_json = self.settings_access.read_settings("mode_settings.json")

        for i in range(len(settings)):
            mode_settings_json["wobble"]["tv_data"][settings[i]] = new_data[i]

        self.settings_access.write_settings("mode_settings.json", mode_settings_json)

    def save_tv_coords(self, tv_area_roi):
        """Saves the TV coordinates in mode settings.

        Parameters:
        -----------
        tv_area_roi : tuple
            A tuple with the top-left corner, width and 
            height of the TV area.

        Returns:
        --------
        None
        """
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
         Parameters:
        -----------
        img : numpy.ndarray
            Image to display
        """
        cv2.imshow(self.name, img)

    def close(self):
        """
        Destroy the OpenCV window
        """
        cv2.destroyWindow(self.name)
