import numpy as np
import pyaudio
# import soundcard as sc
# import soundfile as sf
# # import os
# # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# from keras.models import load_model
# import librosa


class AudioCapture():
    def __init__(self, settings_access, threshold=None) -> None:
        self.threshold = settings_access.read_mode_settings("wobble", "sound_threshold")
        self.buffer_size = 2500#8192
        self.sample_rate = 16000
        self.channels = 1
        self.settings_access = settings_access

        # For moving average
        self.window_size = 5
        self.buffer = np.zeros(self.window_size)


    def set_threshold(self, value):
         self.threshold = value

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
        # print("rms = ", rms)

        if rms > self.threshold:
            return True
        else:
            return False
