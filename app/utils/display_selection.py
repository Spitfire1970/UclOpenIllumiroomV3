from .settings_access import SettingsAccess
from mss import mss
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Entry, IntVar
import screeninfo
import numpy as np
import cv2


class DisplaySelection:

    def __init__(self, settings_access):
        self.settings_access = settings_access
        self.monitor_num_prim = None
        self.monitor_num_proj = None
        self.win = Tk()

    def getImageForTkinter(self,sct,mons):

        disp_image = None

        #Iterate over connected displays
        for num, monitor in enumerate(mons):

            #Take a screenshot from each monitor to display in the tkinter window
            sct_img_whole = np.array(sct.grab(monitor))
            scale_percent = 25 # percent of original size

            heightSCT, widthSCT, channelsSCT = sct_img_whole.shape
            width = int(widthSCT * scale_percent / 100)
            height = int(heightSCT * scale_percent / 100)
            dim = (width, height)
            # resize image to fit in window
            resized = cv2.resize(sct_img_whole, dim, interpolation = cv2.INTER_AREA)

            if disp_image is None:
                disp_image = resized
            else:
                width = disp_image.shape[1]
                #if monitors different resolutions, need to resize resized again
                monitor_res_dif_factor = width/widthSCT

                width = int(widthSCT * monitor_res_dif_factor)
                height = int(heightSCT  * monitor_res_dif_factor)
                dim = (width, height)
                # resize image
                resized = cv2.resize(resized, dim, interpolation = cv2.INTER_AREA)

                disp_image = cv2.vconcat([disp_image, resized])

        height, width, channels = disp_image.shape
        black_image = np.zeros((height,width,4), np.uint8)

        disp_image = cv2.hconcat([disp_image, black_image])
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        fontScale              = 1
        fontColor              = (255,255,255)
        thickness              = 3
        lineType               = 2

        height, width, channels = disp_image.shape
        #Label the display images of the monitors, 1 to n monitors
        for count in range(0,len(mons)):
            textLocation = (int(width*3/4) , int(height/len(mons)/2 + (count*height/len(mons))))
            cv2.putText(disp_image,str(count+1), 
                textLocation,
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)

        return disp_image

    def getMonitorNumWithTkinter(self,disp_image):
          
        #Display the tkinter window until the monitor nums have been entered
        while self.monitor_num_prim is None:
            
            monitor_num_tk_prim = IntVar()
            monitor_num_tk_proj = IntVar()

            #Updated the values on button click
            def get_value():
                monitor_num_tk_prim.set(entryPrim.get())
                monitor_num_tk_proj.set(entryProj.get())

                self.monitor_num_prim = monitor_num_tk_prim.get()
                self.monitor_num_proj = monitor_num_tk_proj.get()
                self.win.destroy()

                
            width, height, channels = disp_image.shape
            geometry_string="%sx%s" % (int(width*2), height)

            self.win.geometry(geometry_string)
            self.win.title('Select Display')
            self.win.attributes('-topmost',1)
            #Load the image

            #Rearrange colors
            blue,green,red,alpha = cv2.split(disp_image)
            img = cv2.merge((red,green,blue))
            im = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=im)
            Label(self.win, image= imgtk).pack()

            #TKinter boxes for monitor number entry
            Label(self.win, text="Please chose your primary monitor by entering the appropriate number ").pack()
            entryPrim = Entry(self.win,font=('Century 12'),width=40)
            entryPrim.pack(pady= 10)
            Label(self.win, text="Please also chose your projector ").pack()
            entryProj = Entry(self.win,font=('Century 12'),width=40)
            entryProj.pack(pady= 10)
            Button(self.win, text="Enter", command= get_value).pack()
            self.win.mainloop()

    def select_tv_projector(self):
        sct = mss()

        #Take a screenshot of all monitors 
        mons = sct.monitors[1:]
        disp_image = self.getImageForTkinter(sct,mons)

        #Get the monitor number from the TKinter window, and set the displays 
        #to the apprpriate mss
        self.getMonitorNumWithTkinter(disp_image)
        displays = {"primary_display":sct.monitors[self.monitor_num_prim],"projector_display":sct.monitors[self.monitor_num_proj]}
        
        #Write the selected displays to the general settings json
        general_settings_json = self.settings_access.read_settings("general_settings.json")
        general_settings_json['selected_displays'] = displays
        self.settings_access.write_settings("general_settings.json", general_settings_json)

        #print("Selected Displays!")
        return displays
