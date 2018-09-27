#! /usr/bin/python3

import argparse

from hill_cipher import decrypt

parser = argparse.ArgumentParser(description = "Implementation of Hill Cipher Decryption")
parser.add_argument("input_file", help = "File containing ciphertext")
parser.add_argument("key", help = "key for Hill cipher encryption")
args = parser.parse_args()
   
try:
    fd_r = open(args.input_file, "r")
    ciphertext = fd_r.read()
    fd_r.close()
except IOError as e:
    print(e)
    raise SystemExit

plainText = decrypt(args.key, ciphertext)

try:
    fd_w = open(args.input_file.split(".")[0] + ".dec", "w")
    fd_w.write(plainText)
    fd_w.close()
except IOError as e:
    print(e)
    raise SystemExit
