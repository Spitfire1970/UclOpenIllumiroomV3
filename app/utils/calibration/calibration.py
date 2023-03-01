import cv2
import itertools
import time
class Calibration:
    
    def __init__(self,settings_access, display_capture):
        self.settings_access = settings_access
        self.projector_resolution = display_capture.get_projector_bounding_box()
        self.cam_port = settings_access.read_general_settings("camera_nr")

        self.gcp = cv2.structured_light.GrayCodePattern.create(self.projector_resolution["width"],
                                                              self.projector_resolution["height"])
        self.image_library_path = self.settings_access.assets_path + "calibration/grey_code_photos/img"

        self.num_images = 5
        self.video_capture = cv2.VideoCapture(self.cam_port,cv2.CAP_DSHOW)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    def capture(self) :
            captured_frames = []
            print("capture")
            
            #black_projection, white_projection = self.gcp.getImagesForShadowMasks(self.projector_resolution,self.projector_resolution)
            
            for res_num in range(self.num_images):
                # reading the input using the camera
                print(res_num)
                #time.sleep(1)
                result, image = self.video_capture.read()
                
                
                # If image will detected without any error, 
                # show result
                if result:
                
            
                    # Save image in local storage
                    cv2.imwrite(self.image_library_path+str(res_num)+".jpg", image)
                
                
                
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