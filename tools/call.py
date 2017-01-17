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
