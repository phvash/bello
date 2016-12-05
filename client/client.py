from tools import connections
from tools import sniffer

# try:
#     username = connections.connect_host('call', host='192.168.43.63')
#     print username
# finally:
#     pass

try:
    connections.connect_host('call', host='127.0.0.1')
finally:
    pass

# def main():
#
#     active_users = sniffer.get_active_users()
#     print "The following Users are active: "
#     for user in active_users.values():
#         print user
#     target = raw_input("Enter a user to call")
#     while target not in active_users.values():
#         print "User not found!"
#
#     try:
#         connections.connect_host(connection_type='call', host=active_users[target])
#     finally:
#         pass


