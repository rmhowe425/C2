import ssl
from utils.Log import Log
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR

'''
    Class responsible for setting up and maintaining a socket 
    server on a specified port. Socket operates over SSL and requires 
    an additional Diffie-Hellman key exchange to set up symmetric crypto.
'''
class SVR:

    '''
        Constructor for the SVR class.
    '''
    def __init__(self):
        self.log = Log()
        self.blackList = []
        self.connections = {}

    '''
        Tears down the socket object that a remote host is 
        using to communicate with the server.
        @param sock: Socket instance to be destroyed.
        @return: True if socket is destroyed.
    '''
    def tearDown(self, sock):
        flag = False
        try:
            sock.shutdown(SHUT_RDWR)
            sock.close()
            del sock # 0 references to sock, object deleted?
            flag = True
        except Exception as e:
            self.log.addToErrorLog("{}\n".format(str(e)))
        return flag

    '''
        Creates an instance of a socket server that uses SSL / TLS.
        Also implements IP Filtering / Logging.
    '''
    def initiate(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('path/to/cabundle.pem')

        with socket(AF_INET, SOCK_STREAM) as s:
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind(('', 8080))
            s.listen(1)
            with context.wrap_socket(s, server_side = True) as ssock:
                conn, addr = ssock.accept()

        # conn, addr if connection is legal
        connection = ('', '')

        # Log connection event dd/mm/YY H:M:S
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.log.addToLog('{} initiated a connection at: {}\n'.format(addr[0], dt_string))

        # IP is blacklisted
        if addr[0] in self.blackList:
            self.tearDown(s)

        # New entry in dictionary
        elif addr[0] not in self.connections:
            self.connections.update({addr[0]: 0})
            connection = conn, addr

        # IP Addr exists, increase connection attempts by 1
        elif addr[0] in self.connections and self.connections.get(addr[0]) < 3:
            self.connections[addr[0]] = self.connections.get(addr[0]) + 1
            connection = conn, addr

        # IP Added to blacklist
        elif addr[0] in self.connections and self.connections.get(addr[0]) == 3:
            self.log.addtoBlackList("{} added to blacklist at {}n".format(addr[0]), dt_string)
            self.tearDown(s)

        return connection








