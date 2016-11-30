import socket


def listen(username, host='127.0.0.1', port=5099):

    s = socket.socket()
    s.bind((host, port))  # argument must be a tuple

    print 'listening on port %s for connections' % port
    s.listen(1)
    # get a connection and address of client
    c, addr = s.accept()
    print 'Connection from: %s' % (str(addr))
    reply(c, username)


# replies with username for dummie connection, video feed for chat request

def reply(connection, username):

    try:
        while True:
            data = connection.recv(1024)
            print 'received "%s"' % data

            if data and 'dummie' in data:
                connection.sendall(username)
                break

            elif data and 'chat' in data:
                print 'live chat started'
                break
    finally:
        # Clean up the connection
        connection.close()


def connect_host(connection_type, host='127.0.0.1', port=5099):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print 'connecting to %s port %s' % (host, port)
    sock.connect((host, port))
    message(host, sock, connection_type)


def message(host, connection, connection_type):

    if connection_type.lower() == 'dummie':

        try:
            # Send connection type
            connection.sendall(connection_type)

            # Look for the response
            username = connection.recv(1024)
            print '%s - %s' % (host, username)

        finally:
            print 'closing socket'
            connection.close()

    elif connection_type.lower() == 'chat':

        try:
            # Send connection type
            connection.sendall(connection_type)

            # starting video feed

        finally:
            connection.close()
