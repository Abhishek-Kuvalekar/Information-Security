#! /usr/bin/python3
import socket
from myencryption import encrypt

print("Welcome!")
print("Enter your credentials: ")
s = None
    
print("Username: ", end = "")
username = input()
print("Password: ", end = "")
password = input()
encryptedString = encrypt(username) + "\n" + encrypt(password)
    
if s == None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 29497
    s.connect(('127.0.0.1', port))
    
s.send(encryptedString.encode())
reply = s.recv(1024)
if "success" in reply.decode().lower():
    print("Correct Login Credentials!")
else:  
    print("Incorrect Login Credentials! Try again!")
s.close()
