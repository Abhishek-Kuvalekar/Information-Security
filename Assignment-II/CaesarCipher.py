#! /usr/bin/python3

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
    print("Enter shift: ", end = "")
    while True:
        try:
            shift = int(input())
            break
        except:
            print("Invalid shift.\nEnter shift again: ", end = "")
    
    print("Enter plain text. Press Ctrl-D to exit.")
    while True:
        try:
            plainText = input()
            cipherText = encrypt(plainText, shift)
            decryptedText = decrypt(cipherText, shift)
            print("Plain Text = " + plainText)
            print("Cipher Text = " + cipherText)
            print("Decrypted Text = " + decryptedText)
        except EOFError:
            break

if __name__ == '__main__':
    main()
