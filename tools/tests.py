from nconnections import Receiver, Sender
from videofeed import SendVideoFeed, ReceiveVideoFeed
import threading


class Send(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Sending message"
        conn = Sender(ip='192.168.43.1', port=6651)
        conn.send('Hello World!')
        reply = conn.receive_reply()
        print reply
        conn.send('You spelt Google wrong hahaha')
        reply = conn.receive_reply()
        print reply
        conn.end()


class Receive(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Receiving Message"
        conn = Receiver(ip='0.0.0.0', port=6651)
        reply = conn.receive()
        print conn.sender_details, '\n'
        print reply
        conn.send_reply('Hello Goolge!')
        reply = conn.receive()
        print reply
        conn.send_reply('Whatever')
        conn.end()


class TestRecVideo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def start(self):
        test = ReceiveVideoFeed()
        test.start()


class TestSendVideo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def start(self):
        test = SendVideoFeed()
        test.start()


if __name__ == '__main__':
    jobs = []

    # print "Test 1: "
    # try:
    #
    #     receiver = Receive()
    #     jobs.append(receiver)
    #     receiver.start()
    #     sender = Send()
    #     jobs.append(sender)
    #     sender.start()
    #
    # except:
    #     print ('Test Failed!')
    #     raise

    print "Test 2"
    try:
        testRecVid = TestRecVideo()
        jobs.append(testRecVid)
        testSendVid = TestSendVideo()
        jobs.append(testSendVid)
    finally:
        pass
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
