import sounddevice as sd
import numpy as np
import time

# duration = 10 # in seconds, must be int
# fs = 48000 # 44100 or 48000 frames per second


def makeRecording(duration=10, fs=48000):
	raw_vr = sd.rec(duration * fs, samplerate=fs, channels=2)
	sd.wait()
	return raw_vr.tostring()

def playRecording(string_data, fs=48000, data_type = 'float32'):
	reconstructed_data = np.fromstring(string_data, data_type)
	sd.play(reconstructed_data, fs)
	sd.wait()

def test():
	a = makeRecording()
	playRecording(a)

if __name__ == '__main__':
	test()