<<<<<<< HEAD
from videofeed import SendVideoFeed, ReceiveVideoFeed
from audtest import AudioSender, AudioReceiver


class Call:
    def __init__(self, **kwargs):
        self.job_queue = []
        self.ip = kwargs.get('ip', None)
        self.vid_recv_port = kwargs.get('vid_recv_port', None)
        self.aud_recv_port = kwargs.get('aud_recv_port', None)
        self.vid_send_port = kwargs.get('vid_send_port', None)
        self.aud_send_port = kwargs.get('aud_send_port', None)
        self.caller_id = kwargs.get('caller_id', None)

    def start(self):
        # video
        vid_recv = ReceiveVideoFeed(port=self.vid_recv_port, caller_id=self.caller_id)
        vid_send = SendVideoFeed(ip=self.ip, port=self.vid_send_port)
        self.job_queue.append(vid_recv)
        self.job_queue.append(vid_send)
        vid_recv.start()
        vid_send.start()

        # audio
        aud_recv = AudioReceiver(port=self.aud_recv_port)
        aud_send = AudioSender(ip=self.ip, port=self.aud_send_port)
        self.job_queue.append(aud_recv)
        self.job_queue.append(aud_send)
        aud_recv.start()
        aud_send.start()

        # wait till call is over
        for thread in self.job_queue:
            thread.join()
=======
import threading
import cv2
import numpy
import socket


class Call:
	def __init__(self, vid_recv_port, vid_send_port, client_ip='localhost'):
		self.client_ip = client_ip
		self.job_queue = []
		self.vid_recv_port = vid_recv_port
		self.vid_send_port = vid_send_port
	def start(self):
		svf_obj = send_video_feed(self.vid_send_port, self.client_ip)
		self.job_queue.append(svf_obj)
		rvf_obj = receive_video_feed(self.vid_recv_port)
		self.job_queue.append(rvf_obj)
		svf_obj.start()
		rvf_obj.start()
		# wait till the jobs are terminated
		for job in self.job_queue:
			job.join()



class send_video_feed(threading.Thread):
	def __init__(self, vid_send_port, target_ip='localhost'):
		threading.Thread.__init__(self)
		self.target_ip = target_ip
		self.port = vid_send_port
		self.cap = cv2.VideoCapture(0)
	    
	def run(self):
	    while True:
	        ret, frame = self.cap.read()
	        rval, imgencode = cv2.imencode(".jpg", frame, [1, 90])
	        data = numpy.array(imgencode)
	        stringData = data.tostring()

	        s = socket.socket()
	        s.connect((self.target_ip, self.port))
	        s.sendall(stringData)

	    s.close()

class receive_video_feed(threading.Thread):
	def __init__(self, vid_recv_port):
		threading.Thread.__init__(self)
		self.port = vid_recv_port


	def run(self):	
		while True:
			host = ''
			port = self.port
			s = socket.socket()
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind((host, port))
			s.listen(1)
			conn, addr = s.accept()
			s_ip, s_port = addr
			
			message = []
			
			while True:
				data = conn.recv(1024 * 1024)
				if not data:
					break
				else:
					message.append(data)
			data = ''.join(message)
			string_data = numpy.fromstring(data, numpy.uint8)

			decimg = cv2.imdecode(string_data, 1)
			cv2.imshow("Bello call from " + s_ip, decimg)

			if cv2.waitKey(5) == 27:
				break
		cv2.destroyAllWindows()

# quick test
if __name__ == '__main__':
	call_obj = Call()
	call_obj.start()
>>>>>>> 5b4c03d89f1d30f77450e6e0bd3cbb4cdade8d83
