import threading
import cv2
import numpy
import socket
import audio


class Call:
    def __init__(self, vid_recv_port, vid_send_port, client_ip='localhost'):
        self.client_ip = client_ip
        self.job_queue = []
        self.vid_recv_port = vid_recv_port
        self.vid_send_port = vid_send_port

    def start(self):
        recv_thread = audio.RecvAud(self.vid_recv_port)
        send_thread = audio.SendAud(self.client_ip, self.vid_send_port)
        self.job_queue.append(recv_thread)
        self.job_queue.append(send_thread)
        recv_thread.start()
        send_thread.start()
        for thread in self.job_queue:
            thread.join()

#
# class send_video_feed(threading.Thread):
#     def __init__(self, vid_send_port, target_ip='localhost'):
#         threading.Thread.__init__(self)
#         self.target_ip = target_ip
#         self.port = vid_send_port
#         self.cap = cv2.VideoCapture(0)
#
#     def run(self):
#         while True:
#             ret, frame = self.cap.read()
#             rval, imgencode = cv2.imencode(".jpg", frame, [1, 90])
#             data = numpy.array(imgencode)
#             stringData = data.tostring()
#
#             s = socket.socket()
#             s.connect((self.target_ip, self.port))
#             s.sendall(stringData)
#
#         s.close()
#
#
# class receive_video_feed(threading.Thread):
#     def __init__(self, vid_recv_port):
#         threading.Thread.__init__(self)
#         self.port = vid_recv_port
#
#     def run(self):
#         while True:
#             host = ''
#             port = self.port
#             s = socket.socket()
#             s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#             s.bind((host, port))
#             s.listen(1)
#             conn, addr = s.accept()
#             s_ip, s_port = addr
#
#             message = []
#
#             while True:
#                 data = conn.recv(1024 * 1024)
#                 if not data:
#                     break
#                 else:
#                     message.append(data)
#             data = ''.join(message)
#             string_data = numpy.fromstring(data, numpy.uint8)
#
#             decimg = cv2.imdecode(string_data, 1)
#             cv2.imshow("Bello call from " + s_ip, decimg)
#
#             if cv2.waitKey(5) == 27:
#                 break
#         cv2.destroyAllWindows()


# test
if __name__ == '__main__':
    call_obj = Call(5610, 6532)
    call_obj.start()
