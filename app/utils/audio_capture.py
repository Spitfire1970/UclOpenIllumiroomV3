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
        pass