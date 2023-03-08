from cv2 import (imread, FONT_HERSHEY_SIMPLEX, putText, imshow, namedWindow,
WINDOW_GUI_NORMAL, moveWindow, waitKey, destroyAllWindows, imwrite)
from ctypes import *
import numpy as np

from .threaded_video_capture import ThreadedVideoCapture


class Calibration:

    def __init__(self, settings_access, display_capture):
        self.settings_access = settings_access
        self.display_capture = display_capture
        self.projector_resolution = self.display_capture.get_projector_bounding_box()
        self.cam_port = settings_access.read_general_settings("camera_nr")

        #Only set up video capture once capture called
        self.video_capture = None
        

        # self.gcp = cv2structured_light.GrayCodePattern.create(self.projector_resolution["width"],
        # self.projector_resolution["height"])
        self.grey_code_image_library_path = self.settings_access.assets_path + "calibration/grey_code_photos/grey_code"
        self.grey_code_source_library_path = self.settings_access.assets_path + "calibration/grey_code_source/grey_code"
        self.instructions_image_library_path = self.settings_access.assets_path + "calibration/instructions/"
        self.room_image_library_path = self.settings_access.assets_path + "room_image/room_img.jpg"

        self.calibration_dll_path = self.settings_access.assets_path + "calibration/ProjectionCalibration.dll"

        self.num_images = 5
        self.confirmed_webcam = False
        self.continue_instructions = False
        self.correct_webcam = False

        self.frame_sleep_time = 1000

        # get intruction images
        self.instruction_image_names = ["place_webcam.jpg", "camera_select.jpg", "grey_code_capture.jpg",
                                        "software_calibration.jpg", "calibration_complete.jpg"]
        self.instruction_images = [
            self.display_capture.frame_primary_resize(imread(self.instructions_image_library_path + img)) for img in
            self.instruction_image_names]

        self.primary_bounding_box = self.display_capture.get_primary_bounding_box()
        self.projector_bounding_box = self.display_capture.get_projector_bounding_box()

        self.confirm_img_text_1 = "Is this the image from the correct webcam? If it is, press 'y' to continue."
        self.confirm_img_text_2 = "If it is not, expecially if a black screen is shown, press 'n'."

        self.captured_frames = []

    def add_confirm_text_to_image(self, img):
        font = FONT_HERSHEY_SIMPLEX
        textLocation1 = (50, 50)
        textLocation2 = (50, 100)
        fontScale = 0.8
        fontColor = (255, 0, 0)
        thickness = 3
        lineType = 2

        putText(img, self.confirm_img_text_1,
                    textLocation1,
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

        putText(img, self.confirm_img_text_2,
                    textLocation2,
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

    def capture_grey_code_images(self):
        # grey code insstructions frame 2
        imshow("Instructions", self.instruction_images[2])

        # set up grey code window
        namedWindow("GreyCode", flags=WINDOW_GUI_NORMAL)  # gui normal makes fullscreen
        calib_dll = cdll.LoadLibrary("ProjectionCalibration.dll")

        calib_dll.capture(self.grey_code_image_library_path.encode(),
                          self.cam_port,
                          self.projector_bounding_box["width"],
                          self.projector_bounding_box["height"],
                          self.primary_bounding_box["left"],
                          self.primary_bounding_box["top"])

    def capture(self):
        
        self.video_capture = ThreadedVideoCapture(self.cam_port)

        namedWindow("Instructions")
        moveWindow("Instructions", self.primary_bounding_box["left"], self.primary_bounding_box["top"])

        # show webcam setup instructions, frame 1
        while not (self.continue_instructions):
            imshow("Instructions", self.instruction_images[0])

            key = waitKey(1)
            if key == 32:  # space key
                self.continue_instructions = True
        destroyAllWindows()
        self.continue_instructions = False

        # black_projection, white_projection = self.gcp.getImagesForShadowMasks(self.projector_resolution,self.projector_resolution)
        test_image = self.video_capture.read()
        room_image = np.copy(test_image)
        # check if any image at all was returned
        imwrite(self.grey_code_image_library_path + "_test.jpg", test_image)
        #self.video_capture.release()
        # check if this is the correct webcam

        while not (self.confirmed_webcam):
            self.add_confirm_text_to_image(test_image)
            namedWindow("Webcam Output")
            moveWindow("Webcam Output", self.primary_bounding_box["left"], self.primary_bounding_box["top"])
            imshow("Webcam Output", self.display_capture.frame_primary_resize(test_image))

            key = waitKey(1)
            if key == ord("n"):
                self.correct_webcam = False
                self.confirmed_webcam = True

                # show webcam selection instructions, frame 1
                while not (self.continue_instructions):
                    imshow("Instructions", self.instruction_images[1])

                    key = waitKey(1)
                    if key == 32:  # space key
                        self.continue_instructions = True
                destroyAllWindows()
                exit()

            elif key == ord("y"):
                self.correct_webcam = True
                self.confirmed_webcam = True
                # write the image taken to the room image, as it is correct, resize to projector resolution
                # room_image_resized = self.display_capture.resize_image_fit_projector_each_frame(test_image)
                # print(room_image_resized.shape)
                imwrite(self.room_image_library_path, room_image)

        destroyAllWindows()

        # # get the grey code images from the webcam
        # if self.correct_webcam:
        #     room_img = self.video_capture.read()
        #     self.captured_frames.append(room_img)
        #     self.capture_grey_code_images()

        #calib_dll = cdll.LoadLibrary(self.calibration_dll_path)
        #calib_dll.calibrate(self.grey_code_image_library_path.encode())
        # show instructions 3
        imshow("Instructions", self.instruction_images[3])
        waitKey(5000)

        # calibration complete! instructions 4
        while not (self.continue_instructions):
            imshow("Instructions", self.instruction_images[4])

            key = waitKey(1)
            if key == 32:  # space key
                self.continue_instructions = True
        destroyAllWindows()

        # calibration complete, exit

        # err, img = cam.read()

        # print(img)

        # waitKey(1000)
        # black_projection, white_projection = self.gcp.getImagesForShadowMasks(self.projector_resolution,
        #                                                                     self.projector_resolution)
        # for projection in itertools.chain(self.gcp.generate()[1], [black_projection, white_projection]):
        #     imshow("img",projection)
        #     waitKey(400)
        #     print("reading camera")
        #     err, img = cam.read()
        #     captured_frames.append(img)
        #     waitKey(400)
        #     self.monitor.display_image(projection, 1)

        # self.monitor.close()
        # return captured_frames[:-2], captured_frames[-2], captured_frames[-1]
