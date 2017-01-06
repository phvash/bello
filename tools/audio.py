import sounddevice as sd
import numpy as np
import socket
import threading
import time


class Player:
    def __init__(self):
        pass

    @staticmethod
    def record(duration=5, fs=48000, channels=2, blocking=True):
        raw_rec = sd.rec(duration * fs,
                         samplerate=fs, channels=channels, blocking=blocking)
        return raw_rec.tostring()

    @staticmethod
    def play(string_data, fs=48000, data_type='float32', blocking=True):
        raw_rec = np.fromstring(string_data, data_type)
        sd.play(raw_rec, fs, blocking=blocking)


class SendAud(threading.Thread):
    def __init__(self, target_ip, port):
        threading.Thread.__init__(self)
        self.target_ip = target_ip
        self.port = port
        # self.aud_str = Player.record()

    def run(self):
        while True:
            aud_str = Player.record()
            s = socket.socket()
            print "connection to " + self.target_ip + 'on' + str(self.port)
            s.connect((self.target_ip, self.port))
            s.sendall(aud_str)
            s.close()


class RecvAud(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.host = ''
        self.port = port
        self.playlist = []
        self.lock = threading.Lock()

    def run(self):

        self.recv_thread = threading.Thread(target=self.receive_audio,  name='recv_aud')
        self.recv_thread.start()

        self.proc_thread = threading.Thread(target=self.process_audio,  name='proc_aud')
        self.proc_thread.start()

    def receive_audio(self):
        while True:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            print "Listening on port", self.port
            s.listen(1)
            conn, addr = s.accept()
            print 'connection from', addr

            received = []  # contains aud_string received in one conn
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    received.append(data)
                    # print "received data"
            aud_str = ''.join(received)
            print 'rebuilt string'
            # self.lock.acquire()
            print "acquire lock"
            self.playlist.append(aud_str)
            print "added str to playlist"
            # self.lock.release()
            print "released lock"
            print "appended"

    def process_audio(self):
        while True:
            # try:
            print "got here"
            # acquired = self.lock.acquire(0)
            if len(self.playlist) > 0:
                current_track = self.playlist[0]
                print "got a track!"
                raw_rec = np.fromstring(current_track, 'float32')
                sd.play(raw_rec, 48000, blocking=True)
                print "played track"
            else:
                time.sleep(5)
                print "no track, retryin in 5"
                continue
            self.playlist.remove(current_track)
                # self.lock.release()
                # if True:
                #     Player.play(current_track)
                #     print "played"
                # else:
                #     pass
            # finally:
            #     if not self.recv_thread.isAlive():
            #         break

if __name__ == '__main__':
    # a = Player.record()
    # Player.play(a)

    queue = []
    recv_thread = RecvAud(7079)
    send_thread = SendAud('127.0.0.1', 7079)
    queue.append(recv_thread)
    queue.append(send_thread)
    recv_thread.start()
    send_thread.start()
    for thread in queue:
        thread.join()
