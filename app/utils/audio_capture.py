
import numpy as np
import pyaudio
# import soundcard as sc
# import soundfile as sf
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
# import librosa


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
        Captures audio input and returns True if the RMS value of the input is greater than the threshold
        value; otherwise, returns False.

    is_loud(data: bytes) -> bool:
        Calculates the RMS value of the given audio input and returns True if the RMS value is greater than
        the threshold value; otherwise, returns False.
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

    def detect_loud_sound(self):
        """
        Captures audio input and returns True if the RMS value of the input is greater than the threshold
        value; otherwise, returns False.

        Returns:
        --------
        bool:
            True if the RMS value of the input is greater than the threshold value; otherwise, False.
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


    def is_loud(self, data):
        """
        Calculates the RMS value of the given audio input and returns True if the RMS value is greater than
        the threshold value; otherwise, returns False.

        Parameters:
        -----------
        data: bytes
            A bytes object containing the audio input data.

        Returns:
        --------
        bool:
            True if the RMS value of the input is greater than the threshold value; otherwise, False.
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
        


#This is code which we could not include in the compiled version due to incompatibility wiht Nuitka, We leave it 
#So that in futuree when Nuitka can compile soundcard and Librosa we can use it again.
"""
#using old version of audio capture and wobble to allow to compile
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
        print("rms = ", rms)

        if rms > self.threshold:
            return True
        else:
            return False
"""

# import numpy as np
# import pyaudio
# import wave
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# from keras.models import load_model
# from librosa import load
# from librosa.feature import mfcc
# # To read system audio:
# # import soundcard as sc (not supported by Nuitka)
# # import soundfile as sf


# class AudioCapture():
#     def __init__(self, settings_access, threshold=None) -> None:
#         self.buffer_size = 1024
#         self.sample_rate = 44100
#         self.channels = 1
#         self.settings_access = settings_access

#         # for moving average
#         self.window_size = 5
#         self.buffer = np.zeros(self.window_size)

#         # for detecting explosive sounds
#         self.num_rows = 40
#         self.num_columns = 174
#         self.num_channels = 1
#         self.model = None
#         self.output_file_name = self.settings_access.utils_path + "audio_output\\out.wav"
#         # classes based on UrbanSound8K dataset
#         self.classes = ['air_conditioner', 'car_horn', 'children_playing', 
#             'dog_bark', 'drilling', 'engine_idling', 'gun_shot', 
#             'jackhammer','siren', 'street_music']

#         self.load_classifier_model()

#     def set_threshold(self, value):
#          self.threshold = value

#     def get_mic_audio(self, save_to_file=False):
#         if save_to_file:
#             format = pyaudio.paInt16
#         else:
#             format = pyaudio.paFloat32

#         p = pyaudio.PyAudio()
#         # Open a stream
#         stream = p.open(
#             format=format, channels=self.channels, 
#             rate=self.sample_rate, input=True, 
#             frames_per_buffer=self.buffer_size
#         )
#         # Read audio
#         if not save_to_file:
#             data = stream.read(self.buffer_size)
#         else:
#             frames = []
#             duration = 1.5
#             for i in range(0, int(self.sample_rate / self.buffer_size * duration)):
#                 data = stream.read(self.buffer_size)
#                 frames.append(data)
#         # Close the stream
#         stream.stop_stream()
#         stream.close()
#         p.terminate()

#         if save_to_file == True:
#             self.save_audio(p, frames)
#         else:
#             return data

#     def save_audio(self, pyaudio_obj, frames):
#         waveFile = wave.open(self.output_file_name, 'wb')
#         waveFile.setnchannels(self.channels)
#         waveFile.setsampwidth(pyaudio_obj.get_sample_size(pyaudio.paInt16))
#         waveFile.setframerate(self.sample_rate)
#         waveFile.writeframes(b''.join(frames))
#         waveFile.close()


#     def is_loud(self, data):
#         # Calculate RMS of the audio
#         rms = np.sqrt(np.mean(np.frombuffer(data, np.float32)**2))
#         # Add RMS to the buffer
#         self.buffer[:-1] = self.buffer[1:]
#         self.buffer[-1] = rms

#         # moving_average = np.mean(self.buffer)
#         # print("rms = ", rms)

#         if rms > self.threshold:
#             return True
#         else:
#             return False

#     def detect_loud_sound(self):
#         data = self.get_mic_audio()
#         return self.is_loud(data)

#     # def detect_loud_sound(self):
#     #     p = pyaudio.PyAudio()
#     #     # Open a stream
#     #     stream = p.open(
#     #         format=pyaudio.paFloat32, channels=self.channels, 
#     #         rate=self.sample_rate, input=True,
#     #         frames_per_buffer=self.buffer_size
#     #     )
#     #     # Read audio
#     #     data = stream.read(self.buffer_size)
#     #     # Close the stream
#     #     stream.stop_stream()
#     #     stream.close()
#     #     p.terminate()

#     #     return self.is_loud(data)

#     def load_classifier_model(self):
#         model_path = (self.settings_access.ml_models_path + 
#             'weights.best.basic_cnn.hdf5')
#         self.model = load_model(model_path)


#     def extract_features(self, file_name):
#         max_pad_len = 174
#         try:
#             audio, sample_rate = load(file_name, res_type='kaiser_fast')            
#             mfccs = mfcc(y=audio, sr=sample_rate, n_mfcc=40)
#             pad_width = max_pad_len - mfccs.shape[1]
#             mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
#         except Exception as e:
#             print("Error encountered while parsing file: ", file_name)
#             return None

#         return mfccs


#     def get_prediction(self, file_name):
#         prediction_feature = self.extract_features(file_name) 
#         prediction_feature = prediction_feature.reshape(1, 
#             self.num_rows, self.num_columns, self.num_channels)

#         # predict_x=self.model.predict(prediction_feature, verbose=0) 
#         # predicted_vector=np.argmax(predict_x,axis=1)
#         # class_index = (predicted_vector)[0]
#         # predicted_class = self.classes[class_index]
#         predicted_proba_vector = self.model.predict(prediction_feature, verbose=0)
#         predicted_proba = predicted_proba_vector[0]

#         # print("------------------")
#         # for i in range(len(predicted_proba)): 
#         #     print(self.classes[i], "\t\t : ", format(predicted_proba[i], '.32f') )

#         dog_bark = predicted_proba[3]
#         drilling = predicted_proba[4]
#         engine_idling = predicted_proba[5]
#         gun_shot = predicted_proba[6]
#         jackhammer = predicted_proba[7]
#         siren = predicted_proba[8]

#         if (drilling > 0.5
#             or engine_idling > 0.5 or gun_shot > 0.5 
#             or jackhammer > 0.45 or siren > 0.7):
#             return True
#         else:
#             return False

#     def detect_explosive_sound(self):
#         self.get_mic_audio(save_to_file=True)
#         return self.get_prediction(self.output_file_name)


#     # def get_system_audio(self):
#     #     sample_rate = 48000
#     #     duration = 1.5
#     #     with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=sample_rate) as mic:
#     #         # record audio with loopback from default speaker.
#     #         try:
#     #             data = mic.record(numframes=sample_rate*duration)
#     #             # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
#     #             sf.write(file=self.output_file_name, data=data[:, 0], samplerate=sample_rate)
#     #         except TypeError:
#     #             raise TypeError