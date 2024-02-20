from .mode import Mode
from utils.audio_capture import AudioCapture
from utils.settings_access import SettingsAccess
import whisper
import time
from PIL import Image, ImageDraw, ImageFont

class VoiceToText(Mode):

    def __init__(
            self,
            settings_access,
            display_capture,  
            background_img,
            voice_capture
        ):
        self.img = background_img
        self.settings = settings_access
        self.filename = __file__[:__file__.index("utils\\voice_to_text.py")] + "assets\\voice\\empty_voice.wav"
        self.fontroot = __file__[:__file__.index("utils\\voice_to_text.py")] + "assets\\fonts\\Honk\\static"
        self.text = ""
        self.capture = True
        self.capture_time = None
        self.frames = None
        self.voice_capture = voice_capture


    def trancription(self):
        model = whisper.load_model("base")
        filename = self.filename
        result = model.transcribe(filename)
        self.text = result["text"]

    def display_text_with_font(self, text, font_name='Honk-Regular', font_size=50):
        self.frames = []
        img = Image.new('RGB', (1920, 1080), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.fontroot, font_name + ".ttf", font_size)
        d.text((1000,100), text, fill=(0,0,0), font=font)
        self.frames.append(img)

    def trigger(self):
        if self.capture:
            self.voice_capture.capture()
            self.trancription()
            self.display_text_with_font(self.text)
            self.capture = False
            self.capture_time = time.time()
        else:
            if time.time() - self.capture_time > 5:
                self.capture = True
        frames = self.frames
        return frames