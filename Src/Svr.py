from utils.Log import Log
from Src.Route import Route
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
        self.PORT = 8081
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
        # conn, addr if connection is legal
        connection = ('', '')

        with self.route.createController() as controller:
            controller.authenticate(password = 'Richard')
            hostname = self.route.setUpService(controller)
            print(hostname)

            if hostname:
                try:
                    with socket(AF_INET, SOCK_STREAM) as s:
                        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                        s.bind(('', self.PORT))
                        s.listen(1)
                        connection = s.accept()
                        print(connection[1])
                except Exception as e:
                    error = str(e)
                    print(error)
                    self.log.addToErrorLog("Unable to establish a socket connection.\n{}".format(error))
                    exit(1)

                self.log.addToLog('{} initiated a connection.'.format(connection[1][0]))

                # IP is blacklisted
                if connection[1][0] in self.blackList:
                    self.tearDown(s)
                    self.log.addToLog("Black-listed IP {} attempted to connect to the server.".format(connection[1][0]))

                # New entry in dictionary
                elif connection[1][0] not in self.connections:
                    self.connections.update({connection[1][0]: 0})
                    self.log.addToLog("IP {} connected to the server.".format(connection[1][0]))

                # IP Addr exists, increase connection attempts by 1
                elif connection[1][0] in self.connections and self.connections.get(connection[1][0]) < 3:
                    self.connections[connection[1][0]] = self.connections.get(connection[1][0]) + 1
                    self.log.addToLog("IP {} connected to the server.".format(connection[1][0]))

                # IP Added to blacklist
                elif connection[1][0] in self.connections and self.connections.get(connection[1][0]) == 3:
                    self.tearDown(s)
                    self.log.addtoBlackList(connection[1][0])
                    self.log.addToLog("IP {} added to the blacklist.".format(connection[1][0]))

        return connection
