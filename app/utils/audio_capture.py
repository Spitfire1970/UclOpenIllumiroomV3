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
import numpy as np
import pyaudio
import soundcard as sc
import soundfile as sf
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
import librosa


class AudioCapture():
    def __init__(self, settings_access, threshold=None) -> None:
        self.threshold = 0
        self.buffer_size = 2500#8192
        self.sample_rate = 16000
        self.channels = 1
        self.settings_access = settings_access

        # For moving average
        self.window_size = 5
        self.buffer = np.zeros(self.window_size)

        # for detecting explosive sound
        self.num_rows = 40
        self.num_columns = 174
        self.num_channels = 1
        self.model = None
        self.output_file_name = self.settings_access.utils_path + "audio_output\out.wav"
        self.classes = ['air_conditioner', 'car_horn', 'children_playing', 
            'dog_bark', 'drilling', 'engine_idling', 'gun_shot', 
            'jackhammer','siren', 'street_music']

        self.load_classifier_model()

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


    def load_classifier_model(self):
        model_path = (self.settings_access.utils_path + 
            'ml_models\weights.best.basic_cnn.hdf5')
        self.model = load_model(model_path)
        # write model to JSON mode settings file

    def get_classier_model(self):
        # get model from JSON mode settings file
        # and save to self.model
        pass


    def extract_features(self, file_name):
        max_pad_len = 174
        try:
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')            
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            pad_width = max_pad_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
            
        except Exception as e:
            print("Error encountered while parsing file: ", file_name)
            return None 

        return mfccs


    def get_prediction(self, file_name):
        prediction_feature = self.extract_features(file_name) 
        prediction_feature = prediction_feature.reshape(1, 
            self.num_rows, self.num_columns, self.num_channels)

        predict_x=self.model.predict(prediction_feature, verbose=0) 
        predicted_vector=np.argmax(predict_x,axis=1)
        class_index = (predicted_vector)[0]
        predicted_class = self.classes[class_index]

        predicted_proba_vector = self.model.predict(prediction_feature, verbose=0)
        predicted_proba = predicted_proba_vector[0]

        print("------------------")
        for i in range(len(predicted_proba)): 
            print(self.classes[i], "\t\t : ", format(predicted_proba[i], '.32f') )
        
        dog_bark = predicted_proba[3]
        drilling = predicted_proba[4]
        engine_idling = predicted_proba[5]
        gun_shot = predicted_proba[6]
        jackhammer = predicted_proba[7]
        siren = predicted_proba[8]
        if (dog_bark > 0.65 or drilling > 0.5
            or engine_idling > 0.5 or gun_shot > 0.5 
            or jackhammer > 0.45 or siren > 0.7):
            return True
        else:
            return False


    def get_system_audio(self):
        sample_rate = 48000
        duration = 1.5
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=sample_rate) as mic:
            # record audio with loopback from default speaker.
            try:
                data = mic.record(numframes=sample_rate*duration)
                # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
                sf.write(file=self.output_file_name, data=data[:, 0], samplerate=sample_rate)
            except TypeError:
                raise TypeError


    def detect_explosive_sound(self):
        try: 
            self.get_system_audio()
            return self.get_prediction(self.output_file_name)
        except TypeError:
            # print("No audio has been detected. Please play a video")
            return False
"""