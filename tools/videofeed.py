import cv2
import numpy
import socket


def send_video_feed(host=None):

    cap = cv2.VideoCapture(0)

    while True:
        if host is None:
            host = 'localhost'
        port = 5565
        ret, frame = cap.read()
        rval, imgencode = cv2.imencode(".jpg", frame, [1, 90])
        data = numpy.array(imgencode)
        stringData = data.tostring()

        s = socket.socket()
        s.connect((host, port))
        s.sendall(stringData)

    s.close()


def receive_video_feed():

    host = ''
    port = 5565

    while True:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()

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
        cv2.imshow("Remote Webcam", decimg)

        if cv2.waitKey(5) == 27:
            break

    cv2.destroyAllWindows()