#!/usr/bin/python

from __future__ import print_function
import mysql.connector

print("Username: ", end = "")
username = raw_input()
print("Password: ", end = "")
password = raw_input()

db = mysql.connector.connect(host = "localhost", user = "user", password = "password", database = "database")

cursor = db.cursor()

query = "select * from login where username = '" + username + "' and password = '" + password + "';"

print("Query Used: " + query)

try:
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) > 0:
        print("Login Successful!")
    else:
        print("Invalid Credentials.")
except:
    print("Unable to fetch data.")
