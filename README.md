# C2

**Python-Based Command & Control server.**

* Uses the Stem library to send all communications through Tor.
* Uses diffie-hellman key exchange to set up symmetic encryption.
* Uses AES Cipher Block Chaining mode for symmetric encryption with a 128-bit key that is generated from an MD5 hash.

### Modes of Operation
* Single Server
* Repeater (Statelessly forwards data from one server to another)

**Required Libraries**
Library | Link
------------ | -------------
PyCryptodome | https://pypi.org/project/pycryptodome/
Stem | https://pypi.org/project/stem/
socket | Native
datetime | Native
socks | Native
