# CSE2130 Files and File Structures - Notes
Files are used in programs to store data. That is data often processed by the program to create information usable by the program or user. The main advantage to incorporating files into program is data persistance, which means that the data is available beyond the running of the program.

Files can be used to store deafult settings and startup instructions, which can even be edited by an external editor; they can also be used to store information created by the program for future use.

Another major advantage to implementing files is that those files can have structures that ensure data integrity. Data integrity is the degree of reliability of the data.

# CRUD in Text Files
### Creating Text Files
Creating a text file in python will also grant file write privilages

```python
FILE = open("filename.ext","x")
```
The above function creates a file with the given filename, opens it, and allows write access. However, if there is a file that already exists with the same name, it will allow a FIleExistsError and stop the python interpreter. An alternate is to use write plus setting.

```python
FILE = open("fileName.ext","w")
```
The above methods will overwrite any information with the new information.

NOTE: The program will look for the file relative to it's location from the program file. (Most likely, this will be the project's root/main folder.)

If the information needs to be added to the end of the text file, use the "a" setting (for append).

```python
FILE = open("filename.ext", "a")
```

### Closing a File
While closing a file is not mandatory, the file will remain in computer memory until it is closed. Therefore, to reduce potential memory leaks, files should be closed immediately after they are read or written to.

```python
FILE = open("filename")
#PROCESSING
FILE.close()
```
### Write to a file 
Writing to a text file uses the ```.write(STRING)``` function. It can only write strings to the file.

```python
FILE = open("hellow-world.txt", "w")
FILE.write("Hello World")
FILE.close()
```
### Reading Contents of a Text File
A file that is open in write mode cannot be read and vice versa. To open a file in read mode, use the following.

```python
FILE = open("filename.ext")
TEXT = FILE.read()
FILE.close()
print(TEXT)
```
### Reading Files Line-By-Line
When preserving information in each row of a spreadsheet file, reading the file line-by-line ensures that the overall structure of the tables in maintained.

```python
FILE = open("filename.ext")
A_LIST = FILE.readlines()
FILE.close()
print(A_LIST)
```
NOTE: Formatting characters such as \n will be visiable in the strings created from readlines(). Therefore, the data often requires clean-up of unanticipated charatcers.

### Updating Files
Updating a file requires reading the file to extract the text, then making changes to the text and then overwriting the file with the new text.

```python
FILE = open("filename.ext")
TEXT = FILE.read()
FILE.close()
#Process the data
FILE = open("filename.ext", "w")
FILE.write(TEXT)
FILE.close()
```
### Deleting a File
To delete content within a file, overwrite the content with a blank string.

```python
FILE = open("filename.ext", "w")
FILE.write("")
FILE.close()
```
To delete a file, python requires access to the operating system to ensure appropriate file manage permissions. 

```python
import os
os.remove("filename.ext")
```
## SQLITE in Python 3

SQLite is a library that a small, flash, self-containing, full-features, SQL database engine. __SQL__ stands for Structured Query Language and is often pronounced _sequel_, making SQLite pronounced as "SQ-Lite" or "sequel lite". While many structures of the query language are similar, there are slight deviations between SQL, SQLite, and other database structures.

Databases create, update, store, and manage data. A database can also summarize the data for reporting as information. Information is the _interpretation_ of data for a specific stakeholder.

Databases use _transactions_ to manipulate information. A transaction is a group of tasks that manipluates data and /or retrives information.

Data provide several advantages over traditional text or spreadsheet files to store data:
1. __Concurrency__ where multiple entities can interact with the data at once. Entities in this case can be users, computer programs, or other databases. An _integrated database_ can have multiple applications accessing the same database.
2. __Atomicity__ is the property that states that a transaction preforms all tasks to complete the transaction, or it reverts so that no tasks are completed within the transaction. 
3. __Consistency__ is where transactions cannot fundamentally change the the strucuture of the database (i.e. There is a set of number of columns with specific data in the columns and a transaction cannot change that structure)
4. __Isolation__ is where multiple transactions can occur in parallel, but to not affect each other.
5. __Durability__ is where the data stored in the database can survive system failures.

All these charactistics contribute to data integrity be ensuring _data validation_ and _verification_ with each transaction.

Databased often use a system to manage them (_A database management system (DBMS)_)

## Setup SQLite in Python3
```python
import sqlite3

FILENAME = "databaseName.db"

# Connect to database. If it doesn't exist, this will create
# the file
CONNECTION = sqlite3.connect(FILENAME)

# Cursor is the object that executes the SQL commands
CURSOR = CONNECTION.cursor()
```
### Create a table in SQLite
```python
CURSOR.execute('''
    CREATE TABLE student(
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT
    )
;''')
```
Tables need a __primary key_, which is the unique identifier of each row of data. Each table can only have one primary key and no two can share the same primary key. Each colummn must identify the data type that will appear in that particular column (INTERGER, TEXT, REAL, NUMERIC, BLOB [binary large object... a long binary string])

NOT NULL is a column property that indicates a cell cannot be left blank.

NOTE: Tables within the same database cannot have the same name.

