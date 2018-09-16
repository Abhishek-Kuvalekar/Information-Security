#!/usr/bin/python3
import sys
from collections import OrderedDict

def main():
    if len(sys.argv) != 3:
        print('Usage: ./PlayFair_Decrypt.py <file-name> <key>')
        return

    inputFile = sys.argv[1]
    key = sys.argv[2].lower()

    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    unique_key_string = "".join(OrderedDict.fromkeys(key))

    if unique_key_string.find('i') >= 0 and unique_key_string.find('j'):
        if unique_key_string.find('i') > unique_key_string.find('j'):
            unique_key_string = unique_key_string.replace("j", "")
        else:
            unique_key_string = unique_key_string.replace("i", "")

    unique_key = OrderedDict.fromkeys(unique_key_string)
    remaining_alphabets = set(alphabets) - set(unique_key)

    key_matrix = "".join(unique_key) + "".join(list(sorted(remaining_alphabets))[0:25 - len(unique_key)])

    matrix = [['z' for i in range(0, 5)] for i in range(0, 5)]

    k = 0
    for i in range(0, 5):
        for j in range(0, 5):
            matrix[i][j] = key_matrix[k]
            k += 1

    try:
        fr = open(inputFile, 'r')
        fw = open('decrypted_playfair.txt', 'w')
    except IOError as e:
        print(e)
        return

    for line in fr:
        line = line.replace(" ", "")
        for index in range(0, len(line) - 1, 2):
            char1_case = 0
            char2_case = 0
            if line[index].isupper():
                char1_case = 1
            if line[index + 1].isupper():
                char2_case = 1
            char1 = line[index].lower()
            char2 = line[index + 1].lower()
            for i in range(0, 5):
                for j in range(0, 5):
                    if matrix[i][j] == char1:
                        index1_x = i
                        index1_y = j
                    if matrix[i][j] == char2:
                        index2_x = i
                        index2_y = j
            if index1_x == index2_x:
                if char1_case:
                    char1 = matrix[index1_x][(index1_y - 1)%5].upper()
                else:
                    char1 = matrix[index1_x][(index1_y - 1)%5]
                if char2_case:
                    char2 = matrix[index2_x][(index2_y - 1)%5].upper()
                else:
                    char2 = matrix[index2_x][(index2_y - 1)%5]
            elif index1_y == index2_y:
                if char1_case:
                    char1 = matrix[(index1_x - 1)%5][index1_y].upper()
                else:
                    char1 = matrix[(index1_x - 1)%5][index1_y]
                if char2_case:
                    char2 = matrix[(index2_x - 1)%5][index2_y].upper()
                else:
                    char2 = matrix[(index2_x - 1)%5][index2_y]
            else:
                if char1_case:
                    char1 = matrix[index1_x][index2_y].upper()
                else:
                    char1 = matrix[index1_x][index2_y]
                if char2_case:
                    char2 = matrix[index2_x][index1_y].upper()
                else:
                    char2 = matrix[index2_x][index1_y]
            fw.write(char1)
            fw.write(char2)
            fw.flush()

    fw.close()

if __name__ == '__main__':
    main()
