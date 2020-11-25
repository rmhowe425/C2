## C2

**Python-Based Command & Control server.**

* Uses the Stem library to send all communications through Tor.
* Uses SSL for two-way authentication and Diffie - Hellman to properly set up hybrid encryption.
* Uses an AES Cipher Block Chaining cipher for symmetric encryption with a 128-bit key that is generated from an MD5 hash.
 

**Required Libraries**
Library | Link
------------ | -------------
PyCryptodome | https://pypi.org/project/pycryptodome/
Stem | https://pypi.org/project/stem/
socket | Native
datetime | native
ssl | native




