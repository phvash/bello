import pyaudio
import threading
from nconnections import Receiver, Sender


class AudioSender(threading.Thread):
    # Audio class based on pyAudio and Wave
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.ip = kwargs.get('ip', '0.0.0.0')
        self.port = kwargs.get('port', None)
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)

    # Audio starts being recorded
    def record_and_send(self):
        conn = Sender(ip=self.ip, port=self.port)
        self.stream.start_stream()
        while conn.active:
            data = self.stream.read(self.frames_per_buffer)
            conn.send(data)
        self.stop()

    # Finishes the audio recording therefore the thread too    
    def stop(self):

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    # Launches the audio recording function using a thread
    def run(self):
        self.record_and_send()


class AudioReceiver(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.ip = '0.0.0.0'
        self.port = kwargs.get('port', None)
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      output=True,
                                      frames_per_buffer=self.frames_per_buffer)
        # self.playlist = []

    def receive_and_play(self):
        conn = Receiver(ip=self.ip, port=self.port) # 6784
        while conn.active:
            data = conn.receive()
            self.stream.write(data)
        self.stop()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def run(self):
        self.receive_and_play()

    # def play(self):
    #     while self.conn.active:
    #         track = self.playlist[0]


if __name__ == '__main__':
    jobs = []
    test = AudioReceiver()
    jobs.append(test)
    test.start()
    test2 = AudioSender()
    jobs.append(test2)
    test2.start()
