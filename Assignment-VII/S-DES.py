#!/usr/bin/python3

import argparse

def applyPermutation(text, permutation_type = "initial"):
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    IIP = [4, 1, 3, 5, 7, 2, 8, 6]

    if permutation_type == "initial":
        permutation = IP
    elif permutation_type == "expansion":
        permutation = EP
    elif permutation_type == "p4":
        permutation = P4
    elif permutation_type == "p8":
        permutation = P8
    elif permutation_type == "p10":
        permutation = P10
    elif permutation_type == "final":
        permutation = IIP

    answer = ""
    for index in permutation:
        answer += str(text[index - 1])
    return answer

def splitIntoTwoHalves(text):
    size = len(text)
    return (text[0 : int(size / 2)], text[int(size / 2) : size])

def XOR(text1, text2, bit_format = "08b"):
    return format(int(text1, 2) ^ int(text2, 2), bit_format)

def applySBoxes(text):
    s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
    r0 = int(text[0] + text[3], 2)
    c0 = int(text[1] + text[2], 2)
    r1 = int(text[4] + text[7], 2)
    c1 = int(text[5] + text[6], 2)

    l = format(s0[r0][c0], "02b")
    r = format(s1[r1][c1], "02b")

    return l + r

def shiftLeft(text, shift):
    num = int(text, 2)
    num = num << shift
    return (format(num, "04b"))

def generateKeys(key):
    key = applyPermutation(key, "p10")
    (l, r) = splitIntoTwoHalves(key)
    
    l1 = shiftLeft(l, 1)
    r1 = shiftLeft(r, 1)
    key1 = applyPermutation(l1 + r1, "p8")

    l2 = shiftLeft(l1, 2)
    r2 = shiftLeft(r1, 2)
    key2 = applyPermutation(l2 + r2, "p8")
    
    return (key1, key2)

def encrypt(text, key):
    ciphertext = ""
    for char in text:
        plaintext = format(ord(char), "08b")
        key1, key2 = generateKeys(key)

        plaintext = applyPermutation(plaintext, permutation_type = "initial")
    
        (l1, r1) = splitIntoTwoHalves(plaintext)
        r = applyPermutation(r1, permutation_type = "expansion")
        r = XOR(r, key1)
        r = applySBoxes(r)
        r = applyPermutation(r, permutation_type = "p4")
        r = XOR(r, l1, bit_format = "04b")
    
        (l2, r2) = (r1, r)
        r = applyPermutation(r2, permutation_type = "expansion")
        r = XOR(r, key2)
        r = applySBoxes(r)
        r = applyPermutation(r, permutation_type = "p4")
        r = XOR(r, l2, bit_format = "04b")

        answer = applyPermutation(r + r2, permutation_type = "final")
        ciphertext += chr(int(answer, 2))
    return ciphertext

def decrypt(text, key):
    plaintext = ""
    for char in text:
        ciphertext = format(ord(char), "08b")
        key1, key2 = generateKeys(key)

        ciphertext = applyPermutation(ciphertext, permutation_type = "initial")

        (l1, r1) = splitIntoTwoHalves(ciphertext)
        r = applyPermutation(r1, permutation_type = "expansion")
        r = XOR(r, key2)
        r = applySBoxes(r)
        r = applyPermutation(r, permutation_type = "p4")
        r = XOR(r, l1, bit_format = "04b")

        (l2, r2) = (r1, r)
        r = applyPermutation(r2, permutation_type = "expansion")
        r = XOR(r, key1)
        r = applySBoxes(r)
        r = applyPermutation(r, permutation_type = "p4")
        r = XOR(r, l2, bit_format = "04b")

        answer = applyPermutation(r + r2, permutation_type = "final")
        plaintext += chr(int(answer, 2))

    return plaintext

def openFile(filename, mode):
    try:
        f = open(filename, mode)
        return f
    except IOError as e:
        print(e)
        raise SystemExit

def main():
    parser = argparse.ArgumentParser(description = "Implementation of S-DES.")
    parser.add_argument("option", help = "encrypt for encryption and decrypt for decryption.")
    parser.add_argument("file", help = "file containing text to encrypted/decrypted.")
    parser.add_argument("key", help = "encryption/decryption key")
    args = parser.parse_args()
    
    if len(args.key) != 10:
        print("Error: Key should be 10 bits long.")
        raise SystemExit
    
    content = openFile(args.file, "r").read()
    
    if args.option == "encrypt":
        ciphertext = encrypt(content, args.key)
        openFile(args.file.split(".")[0] + ".enc", "w").write(ciphertext)
    elif args.option == "decrypt":
        plaintext = decrypt(content, args.key)
        openFile(args.file.split(".")[0] + ".dec", "w").write(plaintext)
    else:
        print("Error: Incorrect option. Valid options are encrypt and decrypt")
 

if __name__ == "__main__":
    main()
    #print(encrypt(chr(int("01110010", 2)), "1010000010"))
    #print(decrypt(chr(int(encrypt(chr(int("01110010", 2)), "1010000010"), 2)), "1010000010"))
