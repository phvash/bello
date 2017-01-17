import socket


# class Connect:
#     def __init__(self, **kwargs):
#         self.ip = kwargs.get('ip', '0.0.0.0')
#         self.port = kwargs.get('port', None)
#         self.conn_type = kwargs.get('conn_type', None)
#         self.conn = None
#         self.s = socket.socket()
#         self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.conn_active = False
#
#         if not self.port:
#             raise ValueError('Please specify a port!')
#         if self.conn_type == 'receiver':
#             self.s.bind((self.ip, self.port))
#             self.s.listen(1)
#             self.conn_active = True
#         elif self.conn_type == 'sender':
#             pass
#         else:
#             raise ValueError('Please specify connection type')
#
#     def send(self, data):
#         if not data:
#             raise ValueError('Please pass a message to send!')
#         if self.conn_type == 'receiver':
#             self.conn.sendall(data)
#         else:
#             if not self.conn_active:
#                 self.s.connect((self.ip, self.port))
#             self.s.sendall(data)
#
#     def receive(self):
#         if self.conn_type == 'receiver' and self.conn_active is False:
#             self.s.bind(('0.0.0.0', self.port))
#             self.s.listen(1)
#             self.conn, addr = self.s.accept()
#         elif self.conn_type == 'sender':
#             pass
#
#         chunks = []
#         while True:
#             data_chunk = self.conn.recv(1024)
#             if not data_chunk:
#                 break
#             else:
#                 chunks.append(data_chunk)
#         self.conn_active = True
#         return addr, ''.join(chunks)
#
#     def stop(self):
#         if self.s:
#             self.s.close()
#         if self.conn:
#             self.conn.close()

#
# class Receive:
#     def __init__(self, **kwargs):
#         ip = kwargs.get('ip', '0.0.0.0')
#         port = kwargs.get('port', None)
#         conn_type = 'receiver'
#         self.conn = Connect(ip=ip, port=port, conn_type=conn_type)
#
#     def receive(self):
#         self.addr, self.message = self.conn.receive()
#
#     def send_reply(self, message):
#         self.conn.send(message)
#
#     def end(self):
#         self.conn.stop()
#
#
# class Send:
#     def __init__(self, **kwargs):
#         ip = kwargs.get('ip', '0.0.0.0')
#         port = kwargs.get('port', None)
#         conn_type = 'sender'
#         self.conn = Connect(ip=ip, port=port, conn_type=conn_type)
#
#     def send(self, message):
#         self.conn.send(message)
#
#     def receive_reply(self):
#         self.adrr, self.reply = self.conn.receive()
#
#     def end(self):
#         self.conn.stop()
#

class Receiver:
    def __init__(self, **kwargs):
        ip = '0.0.0.0'
        port = kwargs.get('port', None)
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(1)
        print "Listening on {} {}".format(ip, port)
        self.conn, self.sender_details = s.accept()
        print "Connection from {}".format(self.sender_details)
        self.active = True

    def receive(self):
        try:
            data_chunk = self.conn.recv(1024*1024)
            return str(data_chunk)
        except socket.error:
            self.active = False
            raise

    def send_reply(self, response):
        try:
            self.conn.send(response)
        except socket.error:
            self.active = False
            raise

    def end(self):
        if self.active:
            self.conn.close()


class Sender:
    def __init__(self, **kwargs):
        ip = kwargs.get('ip', '0.0.0.0')
        port = kwargs.get('port', None)
        self.s = socket.socket()
        print "Sending on {} {}".format(ip, port)
        self.s.connect((ip, port))
        # print "Connected successful"
        self.active = True

    def send(self, message):
        try:
            self.s.send(message)
        except socket.error:
            self.active = False
            raise

    def receive_reply(self):
        try:
            reply = self.s.recv(1024*1024)
            return str(reply)
        except socket.error:
            self.active = False
            raise

    def end(self):
        if self.active:
            self.s.close()
