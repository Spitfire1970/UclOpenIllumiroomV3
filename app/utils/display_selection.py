from mss import mss
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Entry, IntVar, TclError
import numpy as np
from cv2 import (resize, vconcat, hconcat, split, 
    merge, putText, INTER_AREA, FONT_HERSHEY_SIMPLEX
)


class DisplaySelection:

    """A class to select and set the primary display and projector for the system.

    This class provides a graphical user interface (GUI) to the user to select the
    primary display and projector, and then returns the settings for those displays.

    Attributes:
    -----------
    settings_access : dict
        A dictionary with settings for the displays on the system.

    monitors_selected : bool
        A flag that indicates if the monitors have been selected.

    monitor_num_prim : int or None
        The monitor number for the primary display.

    monitor_num_proj : int or None
        The monitor number for the projector.

    win : tkinter.Tk
        The main window for the GUI.

    monitor_num_tk_prim : tkinter.IntVar
        The tkinter IntVar for the monitor number of the primary display.

    monitor_num_tk_proj : tkinter.IntVar
        The tkinter IntVar for the monitor number of the projector.
    """

    def __init__(self, settings_access):
        self.settings_access = settings_access
        self.monitors_selected = False
        self.monitor_num_prim = None
        self.monitor_num_proj = None
        self.win = Tk()
        self.monitor_num_tk_prim = IntVar()
        self.monitor_num_tk_proj = IntVar()


    def get_monitor_screenshots(self,sct,mons):
        """Take screenshots of connected monitors and resize them to fit in the tkinter window.

        Parameters:
        -----------
        sct : mss.mss
            The mss object to capture the screen.

        mons : list of dicts
            A list of dictionaries that define the coordinates of each connected monitor.

        Returns:
        --------
        disp_image : numpy.ndarray
            An array with the resized and concatenated screenshots of all connected monitors.
        """

        disp_image = None

        #Iterate over connected displays
        for num, monitor in enumerate(mons):

            #Take a screenshot from each monitor to display in the tkinter window
            sct_img_whole = np.array(sct.grab(monitor))
            scale_percent = 20 # percent of original size

            heightSCT, widthSCT, channelsSCT = sct_img_whole.shape
            width = int(widthSCT * scale_percent / 100)
            height = int(heightSCT * scale_percent / 100)
            dim = (width, height)
            # resize image to fit in window
            resized = resize(sct_img_whole, dim, interpolation = INTER_AREA)

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
                resized = resize(resized, dim, interpolation = INTER_AREA)

                disp_image = vconcat([disp_image, resized])

        height, width, channels = disp_image.shape
        black_image = np.zeros((height,width,4), np.uint8)

        disp_image = hconcat([disp_image, black_image])
        font                   = FONT_HERSHEY_SIMPLEX
        fontScale              = 1
        fontColor              = (255,255,255)
        thickness              = 3
        lineType               = 2

        height, width, channels = disp_image.shape
        #Label the display images of the monitors, 1 to n monitors
        for count in range(0,len(mons)):
            textLocation = (int(width*3/4) , int(height/len(mons)/2 + (count*height/len(mons))))
            putText(disp_image,str(count+1), 
                textLocation,
                font, 
                fontScale,
                fontColor,
                thickness,
                lineType)

        return disp_image


    def get_monitor_nums(self, disp_image):
        """Display the tkinter window and wait for the user to enter the monitor numbers.

        Parameters:
        -----------
        disp_image : numpy.ndarray
            An array with the resized and concatenated screenshots of all connected monitors.

        Returns:
        --------
        None
        """

        width, height, channels = disp_image.shape
        geometry_string="%sx%s" % (int(width*2), height)
        self.win.title('Select Display')
        self.win.geometry(geometry_string)
        # self.win.attributes('-topmost',1)

        # Rearrange colors
        blue, green, red, alpha = split(disp_image)
        img = merge((red, green, blue))
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        Label(self.win, image=imgtk).pack()

        # TKinter boxes for monitor number entry
        Label(self.win, text="Please chose your primary monitor by entering the appropriate number.").pack()
        Label(self.win, text="If the window reopens, then you have entered an invalid " 
            + "monitor number or closed the window too soon.").pack()
       
        vcmd = (self.win.register(self.validate_user_input), '%P')
        entryPrim = Entry(self.win, font=('Century 12'), width=40, validate='key', validatecommand=vcmd)
        entryPrim.pack(pady=10)
        Label(self.win, text="Please also chose your projector.").pack()
        
        entryProj = Entry(self.win, font=('Century 12'), width=40, validate='key', validatecommand=vcmd)
        entryProj.pack(pady=10)
        Button(self.win, text="Enter", command=lambda: self.update_monitor_numbers(entryPrim, entryProj)).pack()

        self.win.mainloop()

    
    def validate_user_input(self, value):
        """Validate the user's inputs for when they 
        enter the primary and project display numbers.

        Parameters:
        -----------
        value : str
            The user input to be validated.

        Returns:
        --------
        bool
            True if the input is valid (empty or numeric), False otherwise.
        """
        return value =="" or value.isnumeric()


    def update_monitor_numbers(self, entryPrim, entryProj):
        """Updates the indicies for the primary and projector monitors 
        based on the user's input in the tkinter window when the Enter button
        is clicked.

        Parameters:
        -----------
        entryPrim : Entry widget
            A tkinter Entry widget for the user's input for primary display.
        entryProj : Entry widget
            A tkinter Entry widget for the user's input for projector display.

        Returns:
        --------
        None
        """

        self.monitor_num_tk_prim.set(entryPrim.get())
        self.monitor_num_tk_proj.set(entryProj.get())

        try:
            self.monitor_num_prim = self.monitor_num_tk_prim.get()
            self.monitor_num_proj = self.monitor_num_tk_proj.get()
            # self.monitors_selected = True
            self.win.destroy()
        except TclError as e:
            if 'expected floating-point number but got ""' in str(e):
                pass


    def select_tv_projector(self):
        """Select the primary display and projector and return their settings.

        This method takes screenshots of all connected monitors and displays them in a tkinter
        window. It waits for the user to enter the monitor numbers for the primary display and
        projector, and then returns their settings as a dictionary.

        Returns:
        --------
        displays : dict
            A dictionary with the settings for the primary display and projector.
        """
        
        sct = mss()

        #Take a screenshot of all monitors 
        mons = sct.monitors[1:]
        disp_image = self.get_monitor_screenshots(sct,mons)

        while(not(self.monitors_selected)):
            #Get the monitor number from the TKinter window, and set the displays 
            #to the apprpriate mss
            self.get_monitor_nums(disp_image)
            if (self.monitor_num_prim is not None and self.monitor_num_proj is not None
                and self.monitor_num_prim > 0 and self.monitor_num_proj > 0
                and self.monitor_num_prim <=len(mons) 
                and self.monitor_num_proj <=len(mons)
                # for when there's only 1 display
                and (self.monitor_num_prim == 1 or (self.monitor_num_prim != self.monitor_num_proj))):
                
                #Valid monitor numbers entered
                self.monitors_selected = True
                
            else:
                self.monitors_selected = False
                self.win = Tk()

        displays = {"primary_display":sct.monitors[self.monitor_num_prim],"projector_display":sct.monitors[self.monitor_num_proj]}
        
        #Write the selected displays to the general settings json
        general_settings_json = self.settings_access.read_settings("general_settings.json")
        general_settings_json['selected_displays'] = displays
        self.settings_access.write_settings("general_settings.json", general_settings_json)

        return displays
