import pyaudio
import wave

class VoiceCapture():
    def __init__(self, settings_access) -> None:
        self.buffer_size = 1024
        self.sample_rate = 44100
        self.channels = 1
        self.settings_access = settings_access
        self.root = __file__[:__file__.index("utils\\voice_capture.py")]
        self.duration = 5

    def capture(self):
        filename = self.root + "assets\\voice\\empty_voice.wav"
        p = pyaudio.PyAudio()
        # Open a stream
        stream = p.open(
                        format=pyaudio.paFloat32, channels=self.channels, 
                        rate=self.sample_rate, input=True, 
                        frames_per_buffer=self.buffer_size
                        )
        frames = []
        print("Recording...")
        for _ in range(0, int(self.sample_rate / self.buffer_size * self.duration)):
            data = stream.read(self.buffer_size)
            frames.append(data)
        print("Finished recording.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()