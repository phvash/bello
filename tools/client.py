from nconnections import Sender
from config import Details
import call
import sniffer


class Client:
    def __init__(self):
        self.username = Details.get_username()

    def dialer(self):
        print "Scanning network for active users ..."
        active_users = sniffer.get_active_users()
        if len(active_users) != 0:
            print "The following User(s) are active: "
            for user in active_users.keys():
                print user
            target = raw_input("Enter a user to call: ")
            while target not in active_users.keys():
                print "User not found!"
                target = raw_input("Enter a user to call: ")
            self.dial(active_users[target], target)

    def dial(self, ip, contact_id):
        print "Calling {} ...".format(contact_id)
        conn = Sender(ip=ip, port=9482)
        conn.send('call'+self.username)
        reply = conn.receive_reply()
        if reply == 'successful':
            print "Successful! {} received your call".format(contact_id)
            self.make_call(ip)
        elif reply == 'busy':
            print "Sorry, User {} rejected your call".format(contact_id)

    @staticmethod
    def make_call(ip):
        current_call = call.Call(ip=ip, vid_recv_port=6652, aud_recv_port=7752, vid_send_port=6651, aud_send_port=7751)
        current_call.start()

    def start(self):
        self.dialer()
