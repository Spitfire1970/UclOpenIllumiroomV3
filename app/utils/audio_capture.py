
import numpy as np
import pyaudio


class AudioCapture():
    """
    Class for capturing audio input and detecting loud sound events.

    Attributes:
    -----------
    threshold: float
        A value representing the threshold RMS value for detecting loud sound events.
    buffer_size: int
        An integer value representing the buffer size for the PyAudio stream.
    sample_rate: int
        An integer value representing the sample rate of the audio input.
    channels: int
        An integer value representing the number of channels in the audio input.
    settings_access: object
        An object of type SettingsAccess used to access settings.
    window_size: int
        An integer value representing the window size for the moving average filter.
    buffer: numpy.ndarray
        A numpy array of size window_size representing the buffer for the moving average filter.

    Methods:
    --------
    set_threshold(value: float) -> None:
        Sets the threshold RMS value for detecting loud sound events.

    detect_loud_sound() -> bool:
        Captures audio input from the microphone and
        checks if a loud sound is present in the audio data.

    is_loud(data: bytes) -> bool:
        Calculates the RMS value of the given audio input and returns 
        True if the RMS value is greater than the threshold value; 
        otherwise, returns False.
    """
    def __init__(self, settings_access, threshold=None) -> None:
        self.threshold = settings_access.read_mode_settings("wobble", "sound_threshold")
        self.buffer_size = 8096
        self.sample_rate = 16000
        self.channels = 1
        self.settings_access = settings_access

        # For moving average
        self.window_size = 5
        self.buffer = np.zeros(self.window_size)


    def set_threshold(self, value):
         self.threshold = value


    def is_loud(self, data):
        """Determine if the RMS of the audio data exceeds 
        a certain threshold.
        
        Parameters:
        -----------
        data : bytes
            The audio data as bytes.
        
        Returns:
        --------
        bool
            True if the RMS of the audio data exceeds 
            the threshold, False otherwise.
        """
        # Calculate RMS of the audio
        rms = np.sqrt(np.mean(np.frombuffer(data, np.float32)**2))
        # Add RMS to the buffer
        self.buffer[:-1] = self.buffer[1:]
        self.buffer[-1] = rms

        #moving_average = np.mean(self.buffer)
        print("rms = ", rms)

        if rms > self.threshold:
            return True
        else:
            return False


    def detect_loud_sound(self):
        """
        Captures audio input from the microphone and
        checks if a loud sound is present in the audio data.

        Returns:
        --------
        bool:
            True if a loud sound is present, False otherwise.
        """
         
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
