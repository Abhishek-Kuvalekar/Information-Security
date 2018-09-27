#! /usr/bin/python3

import argparse

from hill_cipher import encrypt

parser = argparse.ArgumentParser(description = "Implementation of Hill Cipher")
parser.add_argument("input_file", help = "File containing plaintext")
parser.add_argument("key", help = "key for Hill cipher encryption")
args = parser.parse_args()
   
try:
    fd_r = open(args.input_file, "r")
    plaintext = fd_r.read()
    fd_r.close()
except IOError as e:
    print(e)
    raise SystemExit

cipherText = encrypt(args.key, plaintext)

try:
    fd_w = open(args.input_file.split(".")[0] + ".enc", "w")
    fd_w.write(cipherText)
    fd_w.close()
except IOError as e:
    print(e)
    raise SystemExit
