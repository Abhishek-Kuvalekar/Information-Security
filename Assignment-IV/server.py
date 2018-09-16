#! /usr/bin/python3
import socket
import re
from myencryption import decrypt

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 29497

s.bind(('', port))

s.listen(1)

sock, address = s.accept()

encryptedString = sock.recv(1024).decode()

try:
    username, password = encryptedString.split('\n')
    if re.match("abhishek", decrypt(username)) != None:
        if re.match("111508043", decrypt(password)) != None:
            print("Success!")
            sock.send("Successful!".encode())
        else:
            sock.send("Failed!".encode())
    else:
        sock.send("Failed!".encode())
except:
    print("Failed!")
    sock.send("Failed!".encode())
sock.close() 
s.close()
