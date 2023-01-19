# Chatty Room: A secure Chatroom
This is an application made by Asma Smida & Salma Yahyaoui with python using the security package Crypto and it consists of 3 main parts:
  - Registration/Authentication
  - Secured chatroom with gui made with tkinter
  - Security operations


### Registration/Authentication
- the user can create an accout, that will generate a ciphered token
- When authenticating, users need to present their ciphered token in order to proceed to the application.

### Secured chatroom with tkinter GUI:
- The chatroom consists of a server that stays running and clients that connect
to the server using a pair of keys and send ciphered messages to each other that are deciphered upon receiving, the user can send a message to the server, than the server broadcasts it to the other connected clients.

### Security tools
This app provides tools for various security needs such as:
  - Hashing messages with MD5, SHA-1 or SHA256
  - Symetric ciphering of messages with DES or AES256
  - Assymetric ciphering of messages with RSA or ElGamal
  ## Demo Video


https://user-images.githubusercontent.com/80569527/213578114-49af6c0b-e29a-45b3-b531-0a6b359244f1.mp4

