import unittest
from Src.Crypt import Crypt

'''
    Tests the functionality of the methods within the Crypt() class
'''
class MyTestCase(unittest.TestCase):

    '''
        Tests for correct functionality of the Crypt() class constructor
    '''
    def testConstructor(self):
        inst = Crypt(b"ABC123")
        self.assertIsNotNone(inst.hashKey)
        self.assertIsNotNone(inst.masterKey)
        self.assertIsNotNone(inst.encryptCipher)
        self.assertIsNotNone(inst.decryptCipher)
        self.assertIsNotNone(inst.masterCipher)

    '''
        Tests for correct functionality of the generateHash method in the Crypt() class.
    '''
    def testGenerateHash(self):
        inst = Crypt(b"ABC123")
        inst2 = Crypt(b'')

        h1 = inst.generateHash(b"ABC123")
        h2 = inst.generateHash(b"")

        # Verify hash is 512 bit
        self.assertEqual(len(h1), 16)
        self.assertEqual(len(h2), 16)

        # Verify that same input == same output
        self.assertEqual(inst.hashKey, h1)
        self.assertEqual(inst2.hashKey, h2)
        self.assertEqual(h1, inst.generateHash(b"ABC123"))
        self.assertEqual(h2, inst2.generateHash(b""))

        # Verify that different input != same output
        self.assertNotEqual(h1, inst.generateHash(b"ABC124"))
        self.assertNotEqual(h2, inst.generateHash(b" "))

    '''
        Tests for correct functionality of the encryptData and decryptData methods in the 
        Crypt() class using small length messages.
    '''
    def testEncryptDataAndDecryptData(self):
        inst = Crypt(b"ABC123")

        ct1 = inst.encryptData("A")
        self.assertIsNotNone(ct1)
        self.assertNotEqual(ct1, "A")
        self.assertEqual(len(ct1), 16)

        pt1 = inst.decryptData(ct1)
        self.assertIsNotNone(pt1)
        self.assertEqual(pt1, "A")
        self.assertEqual(len(pt1), 1)

        ct2 = inst.encryptData("Hello. My name is Richard")
        self.assertIsNotNone(ct2)
        self.assertNotEqual(ct2, "Hello. My name is Richard")
        self.assertEqual(len(ct1), 16)

        pt2 = inst.decryptData(ct2)
        self.assertIsNotNone(pt2)
        self.assertEqual(pt2, "Hello. My name is Richard")
        self.assertEqual(len(pt2), len("Hello. My name is Richard"))

        self.assertNotEqual(ct1, ct2)
        self.assertNotEqual(pt1, pt2)

    '''
        Tests for correct functionality of the encryptData and decryptData methods in the 
        Crypt() class using a large message.
    '''
    def testLongMessage(self):
        inst = Crypt(b"123ABC")

        ct = inst.encryptData("A" * 200)
        self.assertIsNotNone(ct)
        self.assertNotEqual(ct, "A" * 200)

        pt = inst.decryptData(ct)
        self.assertIsNotNone(pt)
        self.assertEqual(pt, "A" * 200)
        self.assertEqual(len(pt), len("A" * 200))

    '''
        Tests the functionality of the generateHash method if the input has a length of 0
    '''
    def testEmptyHash(self):
        inst1 = Crypt(b'')
        inst2 = Crypt(b'ABC123')

        ct1 = inst1.encryptData("Hello, my name is Richard.")
        ct2 = inst2.encryptData("Hello, my name is Richard.")

        pt1 = inst1.decryptData(ct1)
        pt2 = inst2.decryptData(ct2)

        self.assertIsNotNone(ct1)
        self.assertIsNotNone(ct2)
        self.assertNotEqual(ct1, ct2)
        self.assertNotEqual(ct1, "Hello, my name is Richard.")
        self.assertNotEqual(ct2, "Hello, my name is Richard.")

        self.assertEqual(pt1, "Hello, my name is Richard.")
        self.assertEqual(pt2, "Hello, my name is Richard.")
        self.assertEqual(pt1, pt2)

    '''
        Tests the functionality of the encrypt/decrypt message method 
        if the input has a length of 0
    '''
    def testEmptyMessage(self):
        inst = Crypt(b'ABC123')
        ct = inst.encryptData('')
        pt = inst.decryptData(ct)

        self.assertIsNotNone(ct)
        self.assertNotEqual(ct, '')
        self.assertEqual(pt, '')
        self.assertEqual(len(pt), len(''))

    '''
        Tests the functionality of the generateHash method in combination with 
        the encrypt/decrypt message method  if the input for all three methods
        has a length of 0
    '''
    def testEmptyHashAndMessage(self):
        inst = Crypt(b'')
        ct = inst.encryptData('')
        pt = inst.decryptData(ct)

        self.assertIsNotNone(ct)
        self.assertEqual(len(ct), 16)
        self.assertNotEqual(ct, '')
        self.assertEqual(pt, '')
        self.assertEqual(len(pt), len(''))

    def testMasterEncrypt(self):
        inst = Crypt(b'')
        ct = inst.masterEncrypt("Hello, my name is Richard.")

        self.assertEqual(inst.masterKey, inst.generateHash(b"D0es_N0t_C0mpute"))
        self.assertIsNotNone(ct)
        self.assertNotEqual(ct, "Hello, my name is Richard.")


if __name__ == '__main__':
    unittest.main()
