import saes as s
#p = chr(int("11010111", 2)) + chr(int("00101000", 2))
p = "Hello, I am Abhishek."
k = chr(int("01001010", 2)) + chr(int("11110101", 2))
print(s.encrypt(p, k))
