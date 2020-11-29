from utils.Log import Log
from stem.control import Controller

'''
    Responsible for setting up and maintaining the Tor service 
    used for anonymous communication.
'''
class Route:

    '''
        Constructor for the Route class.
    '''
    def __init__(self):
        self.log = Log()
        self.c_PORT = 9051
        self.r_PORT = 80
        self.h_PORT = 8081

    '''
        Creates a new tor controller on port 8080
        @return hostname(.onion link) and socket object
    '''
    def createController(self):
        controller = ''
        # Establish port for service
        try:
            controller = Controller.from_port(address = "127.0.0.1", port = self.c_PORT)
        except Exception as e:
            error = "Error setting up connection to Tor"
            self.log.addToErrorLog("Error setting up the tor controller.\n{}".format(str(error)))
            exit(1)

        return controller

    '''
        Creates a new hidden service on a specified port 
        @param controller: Controller object that will be hosting the service 
        @return: Hostname (onion link) of the new service.
    '''
    def setUpService(self, controller):
        result = ''

        try:
            # Each service must have an associated folder, result is hidden service hostname
            result = controller.create_ephemeral_hidden_service(self.h_PORT, key_type = 'NEW', key_content = 'RSA1024'
                ,discard_key = False, detached = False, await_publication = False, timeout = None, basic_auth = None, max_streams = None)
        except Exception as e:
            error = str(e)
            self.log.addToErrorLog('Unable to determine hidden service hostname\n{}'.format(error))
            exit(1)

        return result.hostname






