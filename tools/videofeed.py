import threading
from nconnections import Receiver, Sender
import cv2
import numpy


class SendVideoFeed(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.ip = kwargs.get('ip', '0.0.0.0')
        self.port = kwargs.get('port', None)
        self.cap = cv2.VideoCapture(0)

    def run(self):
        self.conn = Sender(ip=self.ip, port=self.port)
        while True:
            ret, frame = self.cap.read()
            rval, imgencode = cv2.imencode(".jpg", frame, [1, 90])
            data = numpy.array(imgencode)
            string_data = data.tostring()
            print "sending: \n {} \n".format(string_data)
            self.conn.send(string_data)


class ReceiveVideoFeed(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.ip = '0.0.0.0'
        self.port = kwargs.get('port', None)
        self.caller_id = kwargs.get('caller_id', None)

    def run(self):
        self.conn = Receiver(ip=self.ip, port=self.port)
        while True:
            data = self.conn.receive()
            print "received: \n {} \n".format(data)
            string_data = numpy.fromstring(data, numpy.uint8)
            print "Coverted received to: \n {} \n".format(string_data)
            decimg = cv2.imdecode(string_data, 1)
            cv2.imshow("Bello call from: {}".format(self.caller_id), decimg)

            if cv2.waitKey(5) == 27:
                break
        cv2.destroyAllWindows()
        self.conn.end()
