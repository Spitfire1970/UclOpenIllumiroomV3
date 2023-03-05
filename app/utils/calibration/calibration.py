import cv2
import itertools
import time
import numpy as np
class Calibration:
    
    def __init__(self,settings_access, display_capture, display_output):
        self.settings_access = settings_access
        self.projector_resolution = display_capture.get_projector_bounding_box()
        self.cam_port = settings_access.read_general_settings("camera_nr")

        #self.gcp = cv2.structured_light.GrayCodePattern.create(self.projector_resolution["width"],
                                                              #self.projector_resolution["height"])
        self.grey_code_image_library_path = self.settings_access.assets_path + "calibration/grey_code_photos/img"
        self.room_image_library_path = self.settings_access.assets_path + "room_image/room_img.jpg"

        self.num_images = 5
        self.correct_webcam = False

        self.frame_sleep_time = 0.2

    def add_text_to_image(self,img,text):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        textLocation           = (50,50)
        fontScale              = 1
        fontColor              = (255,255,255)
        thickness              = 3
        lineType               = 2

        cv2.putText(img,"Is this the correct webcam, If it is, press 'y' to ocntinue. If it is not, press 'n', then selet the next webcam in the launcher.", 
                textLocation,
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)
        

    def capture_grey_code_images(self):
        for res_num in range(self.num_images):
            # reading the input using the camera
            print(res_num)
            #time.sleep(1)
            result, image = self.video_capture.read()
            
            
            
            # If image will detected without any error, 
            # show result
            if result:
            
        
                # Save image in local storage
                cv2.imwrite(self.grey_code_image_library_path+str(res_num)+".jpg", image)
            
    def capture(self) :
            captured_frames = []
            self.video_capture = cv2.VideoCapture(self.cam_port,cv2.CAP_DSHOW)
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            print("capture")
            
            #black_projection, white_projection = self.gcp.getImagesForShadowMasks(self.projector_resolution,self.projector_resolution)
            result, test_image = self.video_capture.read()
            result, test_image = self.video_capture.read()
            #check if any image at all was returned
            if result:
                
                cv2.imwrite(self.grey_code_image_library_path+"_test.jpg", test_image)
                #check if this is the correct webcam
                cv2.imshow("Webcam Output",room_img)

                key = cv2.waitKey(1)
                if key == ord("n"):
                    self.correct_webcam = False

                elif key == ord("y"):
                    self.correct_webcam = True
                
                cv2.destroyAllWindows()

                if (self.correct_webcam):
                    
                    
                    result, room_img = self.video_capture.read()
                    if result:
                        captured_frames.append(room_img)
                        cv2.imwrite(self.room_image_library_path, room_img)

                        self.capture_grey_code_images()
                    time.sleep(self.frame_sleep_time)
                
                
                
            # err, img = cam.read()
            
            # print(img)
            
            # cv2.waitKey(1000)
            # black_projection, white_projection = self.gcp.getImagesForShadowMasks(self.projector_resolution,
            #                                                                     self.projector_resolution)
            # for projection in itertools.chain(self.gcp.generate()[1], [black_projection, white_projection]):
            #     cv2.imshow("img",projection)
            #     cv2.waitKey(400)
            #     print("reading camera")
            #     err, img = cam.read()
            #     captured_frames.append(img)
            #     cv2.waitKey(400)
            #     self.monitor.display_image(projection, 1)

            # self.monitor.close()
            #return captured_frames[:-2], captured_frames[-2], captured_frames[-1]