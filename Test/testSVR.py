import unittest
from time import sleep
from Src.Svr import SVR
from _thread import start_new_thread
from socket import socket, AF_INET, SOCK_STREAM

'''
    Tests the functionality of the methods in the SVR() class.
'''
class MyTestCase(unittest.TestCase):

    def helper(self, inst, sock):
        sleep(2)
        self.assertEqual(inst.tearDown(sock), True)

    '''
        Tests for correct functionality of the SVR() constructor
    '''
    def testConstructor(self):
        inst = SVR()
        self.assertIsNotNone(inst.log)
        self.assertIsNotNone(inst.route)
        self.assertEqual(len(inst.blackList), 0)
        self.assertEqual(len(inst.connections), 0)

    def testInitiate(self):
        inst = SVR()

        connection = inst.initiate()
        self.assertIsNotNone(connection)

if __name__ == '__main__':
    unittest.main()
