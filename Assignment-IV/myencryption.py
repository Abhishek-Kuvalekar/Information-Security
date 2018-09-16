#!/usr/bin/python3
import sys

def openFile(filename, mode):
    try:
        f = open(filename, mode)
    except IOError as e:
        print(e)
    else:
        return f

def decrypt(content):
    plainText = ""
    prev = None
    curr = None
    for character in content.split(", "):
        character = character.strip()
        if(character == ''):
            continue
        curr = int(character)
        if prev == None:
            prev = int(character)
        else:
            curr = (prev - curr)
            prev = curr
        plainText += chr(curr)
    return plainText

def encrypt(content):
    cipherText = ""
    prev = None
    curr = None
    for character in content:
        curr = ord(character)
        if prev == None:
            prev = ord(character)
        else:
            curr = (prev - curr)
            prev = ord(character)
        cipherText += str(curr)
        cipherText += ", "
    return cipherText

def decryptFile(filename):
    fd_r = openFile(filename, "r")
    fd_w = openFile(filename.split(".")[0] + ".dec", "w")
    if (fd_r == None) or (fd_w == None):
        return
    prev = None
    curr = None
    content = fd_r.read()
    for character in content.split(", "):
        character = character.strip()
        if character == '':
            continue
        curr = int(character)
        if prev == None:
            prev = int(character)
        else:
            curr = (prev - curr)
            prev = curr
        fd_w.write(chr(curr))
    fd_r.close()
    fd_w.close()

def encryptFile(filename):
    fd_r = openFile(filename, "r")
    fd_w = openFile(filename.split(".")[0] + ".enc", "w")
    if (fd_r == None) or (fd_w == None):
        return
    prev = None
    curr = None
    for line in fd_r:
        for character in line:
            curr = ord(character)
            if prev == None:
                prev = ord(character)
            else:
                curr = (prev - curr)
                prev = ord(character)
            fd_w.write(str(curr) + ", ")
    fd_r.close()
    fd_w.close()

def showUsage():
    print("Usage: ./encryption.py -d|-e <filename.enc|filename.txt>")

def main():
    if(len(sys.argv) != 3):
        showUsage()
        return
    if(sys.argv[1].lower() == "-e"):
        encryptFile(sys.argv[2])
    elif(sys.argv[1].lower() == "-d"):
        decryptFile(sys.argv[2])
    else:
        showUsage()
        return


if __name__ == '__main__':
    main()
