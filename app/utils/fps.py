from time import time
class FPS:
    def __init__(self):
        self.curr_time = time()

    def get_fps(self):
        curr_fps = round((1/(0.000001+time()-self.curr_time)),1)
        self.curr_time = time()
        return curr_fps

    def print_fps(self):
        print(f"FPS: {self.get_fps()}")