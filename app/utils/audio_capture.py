import numpy as np
import pyaudio


class AudioCapture():
    def __init__(self, threshold=None) -> None:
        self.threshold = threshold
        self.buffer_size = 8192
        self.sample_rate = 16000
        self.channels = 1

        # For moving average
        self.window_size = 5
        self.buffer = np.zeros(self.window_size)

    def detect_loud_sound(self):
        p = pyaudio.PyAudio()
        # Open a stream
        stream = p.open(
                        format=pyaudio.paFloat32, channels=self.channels, 
                        rate=self.sample_rate, input=True, 
                        frames_per_buffer=self.buffer_size
                        )
        # Read audio
        data = stream.read(self.buffer_size)
        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        return self.is_loud(data)

    def is_loud(self, data):
        # Calculate RMS of the audio
        rms = np.sqrt(np.mean(np.frombuffer(data, np.float32)**2))
        # Add RMS to the buffer
        self.buffer[:-1] = self.buffer[1:]
        self.buffer[-1] = rms

        moving_average = np.mean(self.buffer)
        print("rms = ", rms)

        if rms > self.threshold:
            return True
        else:
            return False
