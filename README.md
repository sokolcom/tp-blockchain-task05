# TP BLOCKCHAIN TASK #05
# Pseudo Random Distribution


### What is it? 👀

This program emulates (un-)locking car's doors with car key.  
Secure connecton is established over an insecure channel using [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm).   
Implemented elliptic curve: __Curve25519__ ([curve propeties here](https://safecurves.cr.yp.to/field.html)).


### Communication protocol 📜
1) __HANDSHAKE__: _car key_ initiates connection by sending command (e.g. "Unlock doors") to the _car_;
2) __CHALLENGE__: to make sure that command was sent by the trusted _key_, _car_ sends signed (using __car's private key__) _nonce_ to the _key_;
3) __RESPONSE__: _car key_ verifies car's signature and sends signed (using __key's private key__) _nonce_ back to the _car_;
4) __VALIDATE__: _car_ verifies key's signature and executes command.

![protocol](/images/protocol.png)



### Usage 🌍

1. ⭐ Star this repo.
2. 📂 Clone this repo (e.g. via ```git clone```).
```sh
git clone https://github.com/sokolcom/tp-blockchain-task05.git
```
3. 🚀 Run ```python3 src/main.py``` in the repo directory to run the program.
```sh
python3 src/main.py
```
4 . 🔍 Example output:  
![example](/images/example.png)
