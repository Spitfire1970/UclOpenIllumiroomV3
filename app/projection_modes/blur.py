


from projection_modes.mode import Mode




class Blur(Mode):
    
    def __init__(self):
        self.blur_amount = 1

    def blur(self):
        print("blurring")

    def trigger(self):
        print("trigger blur")

