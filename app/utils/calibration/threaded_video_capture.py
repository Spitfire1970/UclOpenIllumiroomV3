from cv2 import (VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT,
CAP_DSHOW)
import queue
import threading
from numpy.typing import NDArray


class ThreadedVideoCapture:

    def __init__(self, camera_id: int):
        self.camera = VideoCapture(camera_id, CAP_DSHOW)
        self.camera.set(CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(CAP_PROP_FRAME_HEIGHT, 1080)
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._frame_reader, daemon=True)
        self.thread.start()

    def _frame_reader(self):
        """
        Method used internally to read frames in a separate thread, to keep buffer empty
        """
        while self.camera.isOpened():
            result, frame = self.camera.read()
            if not result:
                break
            if not self.queue.empty():
                try:
                    self.queue.get_nowait()
                except queue.Empty:
                    pass
            self.queue.put(frame)

    def opened(self):
        return self.camera is not None and self.camera.isOpened()

    def read(self) -> NDArray:
        """
        Read last frame from camera
        :return: Last camera frame
        """
        return self.queue.get()

    def close(self):
        """
        Close the video stream
        """
        self.camera.release()

