#a_filesactions.py

'''
Title: CRUD in files
Author: Beatrix Bicomong
Date: April 11, 2022
'''

## Creating a file
FILENAME = "crud.txt"

FILE = open(FILENAME, "w")

##Write to a file
FILE.write("Hello World\n")

## Close a file
FILE.close()

## Append to a file
FILE = open(FILENAME, "a")
FILE.write("Good morning!")
FILE.close()

## Read a file
FILE = open(FILENAME)
TEXT = FILE.read()
FILE.close()
print(TEXT)

## Read a File Line-By-Line
FILE = open(FILENAME)
A_LIST = FILE.readlines()
FILE.close()
for i in range(len(A_LIST)):
    if i != len(A_LIST)-1:
        A_LIST[i] = A_LIST[i][:-1]
print(A_LIST)

## Deleting a file
import os
os.remove(FILENAME)








