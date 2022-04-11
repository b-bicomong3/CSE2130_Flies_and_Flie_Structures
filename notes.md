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
