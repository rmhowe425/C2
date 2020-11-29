from datetime import datetime

'''
    Class responsible for logging various actions, events, and errors that
    occur throughout program execution.
'''
class Log:

    '''
        Constructor for the Log class.
    '''
    def __init__(self):
        self.log = 'log.txt'
        self.error = 'errorLog.txt'
        self.blackList = 'blacklist.txt'

    '''
        Create time stamp for error messages.
        Time stamp is in the format: dd/mm/YY H:M:S
    '''
    def getTimeStamp(self):
        return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    '''
        Class responsible for logging normal events such as 
        socket connection, SSL / Diffie-Hellman set up.
        @param: entry: Action that is to be logged.
        @return: True if the event is successfully logged.
    '''
    def addToLog(self, entry):
        status = False
        try:
            with open(self.log, "a+") as file:
                file.write(self.getTimeStamp() + '\n' + "-" * 85 + '\n' + entry + '\n\n')
                status = True
        except Exception as e:
            self.addToErrorLog(str(e))
        return status

    '''
        Class responsible for logging program errors
        @param error: Error message that is to be logged.
        @return: True if the event is successfully logged. 
    '''
    def addToErrorLog(self, error):
        flag = False
        with open(self.error, "a+") as file:
            file.write(self.getTimeStamp() + '\n' + "-" * 85 + '\n' + error + '\n\n')
            flag = True
        return flag

    '''
        Records an IP Address that is to be blacklisted from 
        connecting to the server.
        @param entry: IP Address that is to be logged.
        @return: True if the event is successfully logged.
    '''
    def addtoBlackList(self, entry):
        status = False
        try:
            with open(self.blackList, "a+") as file:
                file.write(self.getTimeStamp() + '\n' + "-" * 85 + '\n' + entry + '\n\n')
                status = True
        except Exception as e:
            self.addToErrorLog(str(e))
        return status