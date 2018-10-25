#!/usr/bin/python3

import argparse

substitutionDictionary = {
            "0000" : "1001",
            "0001" : "0100",
            "0010" : "1010",
            "0011" : "1011",
            "0100" : "1101",
            "0101" : "0001",
            "0110" : "1000",
            "0111" : "0101",
            "1000" : "0110",
            "1001" : "0010",
            "1010" : "0000",
            "1011" : "0011",
            "1100" : "1100",
            "1101" : "1110",
            "1110" : "1111",
            "1111" : "0111"
        }

inverseSubstitutionDictionary = {
            "1001" : "0000",
            "0100" : "0001",
            "1010" : "0010",
            "1011" : "0011",
            "1101" : "0100",
            "0001" : "0101",
            "1000" : "0110",
            "0101" : "0111",
            "0110" : "1000",
            "0010" : "1001",
            "0000" : "1010",
            "0011" : "1011",
            "1100" : "1100",
            "1110" : "1101",
            "1111" : "1110",
            "0111" : "1111"
        }

def substituteNibbles(plaintextMat, inverse = False):
    substitutedMat = list()
    for l in plaintextMat:
        temp = list()
        for nibble in l:
            if not inverse:
                temp.append(substitutionDictionary[nibble])
            else:
                temp.append(inverseSubstitutionDictionary[nibble])
                
        substitutedMat.append(temp)
    return substitutedMat

def shiftRows(plaintextMat):
    plaintextMat[1].reverse()
    return plaintextMat

def mixColumns(plaintextMat, inverse = False):
    lookupTable = {
            "0000" : 0,
            "0001" : 4,
            "0010" : 8,
            "0011" : 12,
            "0100" : 3,
            "0101" : 7,
            "0110" : 11,
            "0111" : 15,
            "1000" : 6,
            "1001" : 2,
            "1010" : 14,
            "1011" : 10,
            "1100" : 5,
            "1101" : 1,
            "1110" : 13,
            "1111" : 9,
        }
    
    inverseLookupTable_2 = {
            "0000" : 0,
            "0001" : 2,
            "0010" : 4,
            "0011" : 6,
            "0100" : 8,
            "0101" : 10,
            "0110" : 12,
            "0111" : 14,
            "1000" : 3,
            "1001" : 1,
            "1010" : 7,
            "1011" : 5,
            "1100" : 11,
            "1101" : 9,
            "1110" : 15,
            "1111" : 13
        }

    inverseLookupTable_9 = {
            "0000" : 0,
            "0001" : 9,
            "0010" : 1,
            "0011" : 8,
            "0100" : 2,
            "0101" : 11,
            "0110" : 3,
            "0111" : 10,
            "1000" : 4,
            "1001" : 13,
            "1010" : 5,
            "1011" : 12,
            "1100" : 6,
            "1101" : 15,
            "1110" : 7,
            "1111" : 14,
        }
    
    if not inverse:
        mixedColumns = [
                [
                    format(int(plaintextMat[0][0], 2)  ^ lookupTable[plaintextMat[1][0]], "08b")[4:8],
                    format(int(plaintextMat[0][1], 2) ^ lookupTable[plaintextMat[1][1]], "08b")[4:8]
                ],
                [
                    format(lookupTable[plaintextMat[0][0]] ^ int(plaintextMat[1][0], 2), "08b")[4:8],
                    format(lookupTable[plaintextMat[0][1]] ^ int(plaintextMat[1][1], 2), "08b")[4:8]
                ]
            ]
    else:
        mixedColumns = [
                [
                    format(inverseLookupTable_9[plaintextMat[0][0]] ^ inverseLookupTable_2[plaintextMat[1][0]], "08b")[4:8],
                    format(inverseLookupTable_9[plaintextMat[0][1]] ^ inverseLookupTable_2[plaintextMat[1][1]], "08b")[4:8]
                ],
                [
                    format(inverseLookupTable_2[plaintextMat[0][0]] ^ inverseLookupTable_9[plaintextMat[1][0]], "08b")[4:8],
                    format(inverseLookupTable_2[plaintextMat[0][1]] ^ inverseLookupTable_9[plaintextMat[1][1]], "08b")[4:8]
                ]
            ]

    return mixedColumns

def addRoundKey(plaintext, key):
    return [
            [str(format((int(str(plaintext[0][0]), 2) ^ int(str(key[0][0]), 2)), "08b")[4:8]), str(format((int(str(plaintext[0][1]), 2) ^ int(str(key[0][1]), 2)), "08b")[4:8])],
            [str(format((int(str(plaintext[1][0]), 2) ^ int(str(key[1][0]), 2)), "08b")[4:8]), str(format((int(str(plaintext[1][1]), 2) ^ int(str(key[1][1]), 2)), "08b")[4:8])]
        ]

def expandKey(key, roundNumber):
    key0 = int(key[0][0] + key[1][0], 2)
    key1 = int(key[0][1] + key[1][1], 2)
    #Nibble substitution of the reverse of the second key
    keyTemp = substitutionDictionary[key[1][1]] + substitutionDictionary[key[0][1]]
    
    if roundNumber == 1:
        rcon = int("10000000", 2)
    elif roundNumber == 2:
        rcon = int("00110000", 2)
    else:
        print("Incorrect round number.")
        raise SystemExit
    
    keyTemp = int(keyTemp, 2) ^ rcon
    
    key2 = key0 ^ keyTemp
    key3 = key1 ^ key2

    return [
            [str(format(key2, '08b')[0:4]), str(format(key3, '08b')[0:4])],
            [str(format(key2, '08b')[4:8]), str(format(key3, '08b')[4:8])]
        ]

def getTextFromMatrix(matrix):
    return chr(int(matrix[0][0] + matrix[1][0], 2)) + chr(int(matrix[0][1] + matrix[1][1], 2))

def createMatrix(text):
    return [
            [str(format(ord(text[0]), '08b')[0:4]), str(format(ord(text[1]), '08b')[0:4])],
            [str(format(ord(text[0]), '08b')[4:8]), str(format(ord(text[1]), '08b')[4:8])]
        ]

def encrypt(plaintext, key):
    ciphertext = ""
    plaintextLength = len(plaintext)
    
    keyMat = createMatrix(key)
    keyMat1 = expandKey(keyMat, 1)
    keyMat2 = expandKey(keyMat1, 2)
    
    i = 0
    while i < plaintextLength:
        if i != plaintextLength - 1:
            plaintextMat = createMatrix(plaintext[i] + plaintext[i + 1])
        else:
            plaintextMat = createMatrix(plaintext[i] + " ")
        i += 2

        plaintextMat = addRoundKey(plaintextMat, keyMat)
        #print(plaintextMat)
        plaintextMat = substituteNibbles(plaintextMat)
        plaintextMat = shiftRows(plaintextMat)
        plaintextMat = mixColumns(plaintextMat)
        plaintextMat = addRoundKey(plaintextMat, keyMat1)

        plaintextMat = substituteNibbles(plaintextMat)
        plaintextMat = shiftRows(plaintextMat)
        plaintextMat = addRoundKey(plaintextMat, keyMat2)
        
        ciphertext += getTextFromMatrix(plaintextMat)
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = ""
    ciphertextLength = len(ciphertext)
    
    keyMat = createMatrix(key)
    keyMat1 = expandKey(keyMat, 1)
    keyMat2 = expandKey(keyMat1, 2)
    
    i = 0
    while i < ciphertextLength:
        if i != ciphertextLength - 1:
            ciphertextMat = createMatrix(ciphertext[i] + ciphertext[i + 1])
        else:
            ciphertextMat = createMatrix(ciphertext[i] + " ")
        i += 2

        ciphertextMat = addRoundKey(ciphertextMat, keyMat2)
        
        ciphertextMat = shiftRows(ciphertextMat)
        ciphertextMat = substituteNibbles(ciphertextMat, inverse = True)
        ciphertextMat = addRoundKey(ciphertextMat, keyMat1)
        ciphertextMat = mixColumns(ciphertextMat, inverse = True)

        ciphertextMat = shiftRows(ciphertextMat)
        ciphertextMat = substituteNibbles(ciphertextMat, inverse = True)
        ciphertextMat = addRoundKey(ciphertextMat, keyMat)

        plaintext += getTextFromMatrix(ciphertextMat)
    return plaintext
    
def openFile(filename, mode):
    try:
        f = open(filename, mode)
        return f
    except IOError as e:
        print(e)
        raise SystemExit

def main():
    parser = argparse.ArgumentParser(description = "Implementation of S-AES.")
    parser.add_argument("option", help = "encrypt for encryption and decrypt for decryption.")
    parser.add_argument("file", help = "file containing text to encrypted/decrypted.")
    parser.add_argument("key", help = "encryption/decryption key")
    args = parser.parse_args()
    
    if len(args.key) != 2:
        print("Error: Key should be 16 bits long.")
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

if __name__ == '__main__':
    main()
