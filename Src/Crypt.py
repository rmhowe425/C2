from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

'''
    Responsible for encrypting and decrypting plaintext information.
    Uses AES Cipher Block Chaining (CBC) for encryption and generates 
    a 128-bit key from an MD5 digest. 
'''
class Crypt:

    '''
        Constructor for the Crypt class.
        @param hk: Input for the MD5 hash used to generate the AES key.
    '''
    def __init__(self, hk):
        self.hashKey = self.generateHash(hk)
        self.masterKey = self.generateHash(b"D0es_N0t_C0mpute")
        self.encryptCipher = self.generateCipher(self.hashKey)
        self.decryptCipher = self.generateCipher(self.hashKey)
        self.masterCipher = self.generateCipher(self.masterKey)

    '''
        @param key: Key used to generate an MD5 digest.
        @return: MD5 digest used as a key for symmetic encryption.
    '''
    def generateHash(self, key):
        h = MD5.new()
        h.update(key)
        return h.digest()

    '''
        Creates an instance of an AES CBC cipher.
        @param key: Key used to create the cipher.
        @return: Instance of an AES CBC cipher.
    '''
    def generateCipher(self, key):
        iv = ('A' * 16).encode('ascii')
        return AES.new(key, AES.MODE_CBC, iv)

    '''
        Encrypts and an arbitrary amount of plain-text data.
        @param pt: Plaintext data to be encrypted.
        @return: The resulting cipher text from the plaintext data. 
    '''
    def encryptData(self, pt):
        return self.encryptCipher.encrypt(pad(pt.encode(), AES.block_size))

    '''
        Decrypts an arbitrary amount of cipher-text data.
        @param pt: Plaintext data to be encrypted.
        @return: The resulting cipher text from the plaintext data. 
    '''
    def decryptData(self, ct):
        return unpad(self.decryptCipher.decrypt(ct), AES.block_size).decode()

    '''
        Encrypts an arbitrary amount of plain-text data.
        Used to encrypt data that is to be received by a host
        that contains the symmetric key.
    '''
    def masterEncrypt(self, pt):
        return self.masterCipher.encrypt(pad(pt.encode(), AES.block_size))