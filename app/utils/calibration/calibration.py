import cv2
import itertools
import time
import numpy as np
class Calibration:
    
    def __init__(self,settings_access, display_capture):
        self.settings_access = settings_access
        self.projector_resolution = display_capture.get_projector_bounding_box()
        self.cam_port = settings_access.read_general_settings("camera_nr")

        #self.gcp = cv2.structured_light.GrayCodePattern.create(self.projector_resolution["width"],
                                                              #self.projector_resolution["height"])
        self.grey_code_image_library_path = self.settings_access.assets_path + "calibration/grey_code_photos/img"
        self.instructions_image_library_path = self.settings_access.assets_path + "calibration/instructions/"
        self.room_image_library_path = self.settings_access.assets_path + "room_image/room_img.jpg"

        self.num_images = 5
        self.confirmed_webcam = False
        self.continue_instructions = False
        self.correct_webcam = False

        self.frame_sleep_time = 0.5

        #intruction images
        self.instruction_images =[cv2.imread(self.instructions_image_library_path+"place_webcam.jpg", 0),]

        self.primary_bounding_box = display_capture.get_primary_bounding_box()
        self.projector_bounding_box = display_capture.get_projector_bounding_box()

        self.confirm_img_text_1 = "Is this the correct webcam? If it is, press 'y' to continue."
        self.confirm_img_text_2 = "If it is not, expecially if a black screen is shown, press 'n', then selet the next or previous webcam in the launcher."

        self.captured_frames = []

    def add_confirm_text_to_image(self,img):
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        textLocation1           = (50,50)
        textLocation2           = (50,100)
        fontScale              = 1
        fontColor              = (255,0,0)
        thickness              = 3
        lineType               = 2

        cv2.putText(img,self.confirm_img_text_1, 
                textLocation1,
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)
        
        cv2.putText(img,self.confirm_img_text_2, 
                textLocation2,
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)
        

    def capture_grey_code_images(self):
        result, image = self.video_capture.read()
        for res_num in range(0,self.num_images+1):
            # reading the input using the camera
            print(res_num-1)
            time.sleep(self.frame_sleep_time)
            result, image = self.video_capture.read()
  
            # If image will detected without any error, 
            # show result
            if result:
            
        
                # Save image in local storage
                cv2.imwrite(self.grey_code_image_library_path+str(res_num-1)+".jpg", image)
            
    def capture(self) :
            
            
            self.video_capture = cv2.VideoCapture(self.cam_port,cv2.CAP_DSHOW)
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            cv2.namedWindow("Instructions")
            cv2.moveWindow("Instructions", self.primary_bounding_box["left"],self.primary_bounding_box["top"])

            #show webcam setup instructions
            while not(self.continue_instructions):
                cv2.imshow("Instructions",self.instruction_images[0])

                key = cv2.waitKey(1)
                if key == 32: #space key
                    self.continue_instructions =True
            cv2.destroyAllWindows()
            self.continue_instructions = False
            
            #black_projection, white_projection = self.gcp.getImagesForShadowMasks(self.projector_resolution,self.projector_resolution)
            result, test_image = self.video_capture.read()
            result, test_image = self.video_capture.read()
            #check if any image at all was returned
            if result:
                
                cv2.imwrite(self.grey_code_image_library_path+"_test.jpg", test_image)
                #check if this is the correct webcam

                while not(self.confirmed_webcam):
                    self.add_confirm_text_to_image(test_image)
                    cv2.namedWindow("Webcam Output")
                    cv2.moveWindow("Webcam Output", self.primary_bounding_box["left"],self.primary_bounding_box["top"])
                    cv2.imshow("Webcam Output",test_image)

                    key = cv2.waitKey(1)
                    if key == ord("n"):
                        self.correct_webcam = False
                        self.confirmed_webcam = True

                    elif key == ord("y"):
                        self.correct_webcam = True
                        self.confirmed_webcam = True
                
                cv2.destroyAllWindows()


                
                if (self.correct_webcam):
                    
                    
                    result, room_img = self.video_capture.read()
                    if result:
                        self.captured_frames.append(room_img)
                        cv2.imwrite(self.room_image_library_path, room_img)

                        self.capture_grey_code_images()
                    
                
                
                
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