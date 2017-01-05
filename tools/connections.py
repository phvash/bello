import socket
# import videofeed
from call import Call


"""
Notes:

A. connection_type:

The client can connect is to the host in two different modes
  i. dummie mode: A test connection to host, returns the username of host if successful
  ii. call mode: starts multiple threads for sending

B. Server and host are used interchangeably to mean the same thing
"""


# replies with username for dummie connection, video feed for chat request
def reply(connection, username, client_address):

    """ responsible for sending replies on behalf host machine """

    client_ip, port = client_address
    try:
        while True:
            data = connection.recv(1024)

            if data and 'dummie' in data:
                connection.sendall(username)
                break

            elif data and 'call' in data:

                call_obj = Call()
                call_obj.start()

                print 'live chat started with'

                # videofeed.send_video_feed(client_ip)
    finally:
        # Clean up the connection
        if connection:
            connection.close()


def get_username(host, connection, connection_type):

    """ used by the client side to connect to a server
    in DUMMIE mode in an attempt to get the username """

    # connection.settimeout(0.01)
    try:
        # Send connection type
        connection.sendall(connection_type)

        # Look for the response
        username = connection.recv(1024)
        print '%s - %s' % (host, username)
        connection.close()
        return username
    finally:
        pass


def connect_host(connection_type, host='127.0.0.1', port=5098):

    """ handles all outgoing connections from the CLIENT to SERVER """

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'connecting to %s port %s' % (host, port)
    # starts a connection with server
    sock.connect((host, port))
    # receives
    if connection_type == 'dummie':
        username = get_username(host, sock, connection_type)
        return username
    elif connection_type == 'call':
        sock.sendall(connection_type)
        # videofeed.receive_video_feed()
        call_obj = Call()
        call_obj.start()


def listen(username, host='127.0.0.1', port=5098):

    """ lives on the HOST,
        handles all incoming connections from CLIENT """

    s = socket.socket()
    s.bind((host, port))  # argument must be a tuple

    while True:
        print 'listening on port %s for connections' % port
        s.listen(1)
        # get a connection and address of client
        c, addr = s.accept()
        print 'Connection from: %s' % (str(addr))
        reply(c, username, addr)
