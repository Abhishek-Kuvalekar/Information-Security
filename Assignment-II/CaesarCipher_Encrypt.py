#! /usr/bin/python3
import sys

def encrypt(plainText, shift):
    plainWords = plainText.split()
    cipherWords = list()
    for word in plainWords:
        cipherWord = ""
        for char in word:
            if char.isalpha():
                if(char.islower()):
                    cipherWord += chr(((ord(char) - 97 + shift) % 26) + 97)
                else:
                    cipherWord += chr(((ord(char) - 65 + shift) % 26) + 65)
            else:
                cipherWord += char

        cipherWords.append(cipherWord)
    cipherText = " ".join(cipherWords)
    return cipherText

def main():
    if len(sys.argv) != 3:
        print("Usage: ./CaesarCipher_Encrypt.py <file-name> <shift>")
        return
    filename = sys.argv[1]
    try:
        fd_r = open(filename, "r")
        fd_w = open("encrypted_caesar.txt", "w")
    except IOError as e:
        print(e)
        return
    
    while True:
        try:
            shift = int(sys.argv[2])
            break
        except:
            print("Integer shift required! Try again!")

    content = fd_r.read()
    content = encrypt(content, shift)
    fd_w.write(content)
    
    fd_r.close()
    fd_w.close()
  

if __name__ == '__main__':
    main()
