#! /usr/bin/python3

import math
import numpy as np

def getModuloInverse(matrix, mod):
    det = int(np.linalg.det(matrix))
    matrix = np.linalg.inv(matrix)
    
    if math.gcd(det, mod) != 1:
        print("Matrix inverse does not exist")
        raise SystemExit
    
    for i in range(1, mod):
        if ((det * i) % mod) == 1:
            for j in range(len(matrix)):
                for k in range(len(matrix[j])):
                    matrix[j][k] = int((matrix[j][k] * i * det)) % 26
            matrix.astype(int)
            return matrix

def getKeyMatrix(key): 
    keyLen = len(key)
    if math.floor(math.sqrt(keyLen)) != math.sqrt(keyLen):
        print("Error: Length of the key must be a perfect square.")
        raise SystemExit

    keyMat = list()
    for letter in key:
        if letter.isupper():
            keyMat.append(ord(letter) - 65)
        elif letter.islower():
            keyMat.append(ord(letter) - 97)
        else:
            print("Error: Key must not contain non-alphanumeric characters.")
            raise SystemExit

    keyMat = np.array(keyMat).reshape(math.floor(math.sqrt(keyLen)), -1)
    return keyMat

def encrypt(key, content):
    cipherText = ""
    keyMat = getKeyMatrix(key)
    letters = list()

    for letter in content:
        if letter.isspace():
            continue
        elif letter.isupper():
            letters.append(ord(letter) - 65)
        elif letter.islower():
            letters.append(ord(letter) - 97)
        else:
            print("Error: File should contain letters and whitespaces only.")
            raise SystemExit
    
    while (len(letters) % math.floor(math.sqrt(len(key)))) != 0:
        letters.append(0)
    letters = np.array(letters).reshape(-1, math.floor(math.sqrt(len(key))))

    for text in letters:
        textMat = np.array(text).reshape(-1, 1)
        result = np.matmul(keyMat, textMat)
        
        for i in range(math.floor(math.sqrt(len(key)))):
            cipherText += chr((result[i][0] % 26) + 65)
    return cipherText

def decrypt(key, content):
    plainText = ""
    keyMat = getModuloInverse(getKeyMatrix(key), 26)
    keyMat = keyMat.astype(int)
    letters = list()

    for letter in content:
        if letter.isupper():
            letters.append(ord(letter) - 65)
        else:
            print("Error: Bad encrypted file. Encrypted file must containg upper case letters only.")
            raise SystemExit
    
    while (len(letters) % math.floor(math.sqrt(len(key)))) != 0:
        letters.append(0)
    letters = np.array(letters).reshape(-1, math.floor(math.sqrt(len(key))))

    for text in letters:
        textMat = np.array(text).reshape(-1, 1)
        result = np.matmul(keyMat, textMat)
    
        for i in range(math.floor(math.sqrt(len(key)))):
            plainText += chr((result[i][0] % 26) + 65)
    return plainText
