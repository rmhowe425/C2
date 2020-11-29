from utils.Log import Log
from Src.Route import Route
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR
from ssl import create_default_context, Purpose,  CERT_REQUIRED

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
        self.route = Route()

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
            self.log.addToErrorLog("Error destroying socket object\n{}".format(str(e)))
        return flag

    '''
        Creates an instance of a socket server that uses SSL / TLS.
        Also implements IP Filtering / Logging.
    '''
    def initiate(self):
        # Make sure tor controller has been created
        controller = self.route.createController()

        # Start hidden service
        self.route.setUpService(controller)

        # Set up SSL configuration
        context = create_default_context(Purpose.CLIENT_AUTH)
        context.verify_mode = CERT_REQUIRED
        context.check_hostname = True

        # Load cert and key files from /artifacts
        try:
            context.load_cert_chain(certfile = '../artifacts/C2.pem', keyfile = '../artifacts/C2.key')
        except Exception as e:
            error = str(e)
            Log.addToErrorLog("Unable to load cert or key files.\n{}".format(error))

        try:
            with socket(AF_INET, SOCK_STREAM) as s:
                s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                s.bind(('', self.route.t_port))
                s.listen(1)
                with context.wrap_socket(s, server_side=True, do_handshake_on_connect=True) as ssock:
                    conn, addr = ssock.accept()
        except Exception as e:
            error = str(e)
            Log.addToErrorLog("Unable to establish an authenticated socket connection.\n{}".format(error))

        # conn, addr if connection is legal
        connection = ('', '')
        self.log.addToLog('{} initiated a connection.'.format(addr[0]))

        # IP is blacklisted
        if addr[0] in self.blackList:
            self.tearDown(s)
            Log.addToLog("Black-listed IP {} attempted to connect to the server.".format(addr[0]))

        # New entry in dictionary
        elif addr[0] not in self.connections:
            self.connections.update({addr[0]: 0})
            connection = conn, addr
            Log.addToLog("IP {} connected to the server.".format(addr[0]))

        # IP Addr exists, increase connection attempts by 1
        elif addr[0] in self.connections and self.connections.get(addr[0]) < 3:
            self.connections[addr[0]] = self.connections.get(addr[0]) + 1
            connection = conn, addr
            Log.addToLog("IP {} connected to the server.".format(addr[0]))

        # IP Added to blacklist
        elif addr[0] in self.connections and self.connections.get(addr[0]) == 3:
            self.tearDown(s)
            self.log.addtoBlackList(addr[0])
            Log.addToLog("IP {} added to the blacklist.".format(addr[0]))

        return connection
