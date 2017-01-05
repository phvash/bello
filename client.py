from tools import connections
from tools import sniffer


def main():
    print "welcome to Bello"
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

        try:
            connections.connect_host(connection_type='call', host=active_users[target])
        finally:
            pass
    else:
        print "No active Bello users found"

if __name__ == '__main__':
    main()