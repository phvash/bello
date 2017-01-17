from nconnections import Receiver
from config import Details
import call

   
class Host:
    def __init__(self):
        self.username = Details.get_username()

    def listen(self):
        conn = Receiver(ip='0.0.0.0', port=9482)
        message = conn.receive()
        if message and 'dummy' in message:
            conn.send_reply(self.username)
            self.listen()
        elif 'call' in message:
            caller_id = message[4:]
            self.notification(conn, caller_id)

    def notification(self, conn, caller_id):
        print "Hello {} , you have call from {} ".format(self.username, caller_id)
        while True:
            response = raw_input("Enter Yes to Accept the Call, No to reject: ").lower()
            if response == 'yes' or response == 'no':
                break
            else:
                print "Invalid Option, Please try again! "

        if response == 'no':
            confirm_reply = "Sure you want to reject the call {} ?\n Yes or No?: ".format(self.username)
            if confirm_reply == 'no':
                conn.send_reply('busy')
            else:
                self.pick_call(conn, caller_id)
        else:
            self.pick_call(conn, caller_id)

    @staticmethod
    def pick_call(conn, caller_id):
        ip, adrrs = conn.sender_details
        conn.send_reply('successful')
        current_call = call.Call(caller_id=caller_id, ip=ip, vid_recv_port=6651, aud_recv_port=7751, vid_send_port=6652, aud_send_port=7752)
        current_call.start()

    def start(self):
        self.listen()
