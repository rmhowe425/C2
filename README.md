## C2

**Python-Based Command & Control server.**

* Uses SSL and Diffie - Hellman for authentication and to securely set up symmetric encryption.
* Uses an AES Cipher Block Chaining cipher for symmetric encryption with a 128-bit key that is generated from an MD5 hash.
* Uses the Stem library to send all communications through Tor. 

**Required Libraries**
Library | Link
------------ | -------------
PyCryptodome | https://pypi.org/project/pycryptodome/
Stem | https://pypi.org/project/stem/
socket | Native
datetime | native
ssl | native




