#! /usr/bin/python3
import sys

def decrypt(cipherText, shift):
    cipherWords = cipherText.split()
    plainWords = list()
    for word in cipherWords:
        plainWord = ""
        for char in word:
            if char.isalpha():
                if(char.islower()):
                    plainWord += chr(((ord(char) - 97 - shift) % 26) + 97)
                else:
                    plainWord += chr(((ord(char) - 65 - shift) % 26) + 65)
            else:
                plainWord += char
        plainWords.append(plainWord)
    plainText = " ".join(plainWords)
    return plainText

def main():
    if len(sys.argv) != 3:
        print("Usage: ./CaesarCipher_Decrypt.py <file-name> <shift>")
        return
    filename = sys.argv[1]
    try:
        fd_r = open(filename, "r")
        fd_w = open("decrypted_caesar.txt", "w")
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
    content = decrypt(content, shift)
    fd_w.write(content)
    
    fd_r.close()
    fd_w.close()
  

if __name__ == '__main__':
    main()
