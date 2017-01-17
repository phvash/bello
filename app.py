from tools.host import Host
from tools.client import Client
from tools.config import Details
import os
# welcome
# Dial,
# Incoming call Notifications,
# Receive or reject
# check existing detail


class Bello:
    def __init__(self):
        if os.path.isfile('settings'):
            self.username = Details.get_username()
            print "Welcome Back to Bello {} ".format(self.username)
        else:
            self.username = raw_input("Welcome to Bello!\n Please enter a username: ")
            Details.set_username(self.username)

    def run(self):
        host = Host()
        client = Client()
        while True:
            response = raw_input("Enter '1 'to run Bello in the background "
                                 " (wait for incoming calls)\nEnter '2' to make a call\n"
                                 "Enter 3 to quit Bello: ")
            try:
                response = int(response)
            except ValueError:
                print "Invalid Option!"
                continue
            try:
                if response == 1:
                    host.start()
                elif response == 2:
                    client.start()
                elif response == 3:
                    print "Bye. See you soon {}".format(self.username)
                    break
                else:
                    print "Invalid Option! "
                    continue
            except KeyboardInterrupt:
                continue

if __name__ == '__main__':
    app = Bello()
    app.run()
