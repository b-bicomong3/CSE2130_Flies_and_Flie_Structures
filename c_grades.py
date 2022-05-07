#c_grades.py
'''
Title: Redo
Author: Beatrix Bicomong
Date: April 14, 2022
'''

### --- VARIABLES --- ###
FILENAME = "c_grade.txt"

### --- INPUT
def getFileRead():
    ''''''

    global FILENAME
    try:
        FILE = open(FILENAME, "x")
        START_GRADE = []
        START_GRADE.append("There are no subjects added yet")
        START_GRADE_TEXT = ",".join(START_GRADE)
        FILE.write(START_GRADE_TEXT)
        FILE.close()
    except FileExistsError:
        pass

    FILE = open(FILENAME)

    return FILE

def  menu():
    """User chooses the opertation

    Returns:
        CHOICE (int):
    """

    print("""
1. View grade
2. Add subject    
3. Update subject
4. Delete subject
5. Calculte average
6. Exit    
    """)

    CHOICE = input("> ")

    if CHOICE.isnumeric():
        CHOICE = int(CHOICE)
    else:
        print("Please enter a number!")

        return menu()
    if 0 < CHOICE < 7:

        return CHOICE
    else:
        print("Please enter a number in the menu")

        return menu()

def getGrade():
    ''''''
    GRADE = input("Grade: ")

    if GRADE.isnumeric():
        return int(GRADE)
    else:
        print("Please enter a number")
        return getGrade()

def getSubject():
    ''''''
    SUBJECT = input("Subject: ")
    return SUBJECT
    
### --- PROCESSING
def readFile(FILE_OBJ):
    ''''''
    TEXT = FILE_OBJ.read()
    FILE_OBJ.close()
    GRADE_ARRAY = TEXT.split(",")

    return GRADE_ARRAY

def addSubject(GRADE, SUBJECT, GRADE_ARRAY):
    ''''''
    GRADE_ARRAY_2D = []

    for i in range(len(GRADE_ARRAY)):
        GRADE_ARRAY_2D.append(GRADE_ARRAY[i].split())

    GRADE_ARRAY.insert(i, f"{SUBJECT} {GRADE}")

    for i in range(len(GRADE_ARRAY)):
        if GRADE_ARRAY[i] == "" or GRADE_ARRAY[i] == "There are no subjects added yet":
            GRADE_ARRAY.pop(i)

    return GRADE_ARRAY

def updateGrade(GRADE_ARRAY):
    ''''''
    print(GRADE_ARRAY)

    GRADE_ARRAY_2D = []

    for i in range(len(GRADE_ARRAY)):
        GRADE_ARRAY_2D.append(GRADE_ARRAY[i].split())
    
    SELECT = input("Select subject: ")

    for i in range(len(GRADE_ARRAY_2D)):
        if GRADE_ARRAY_2D[i][0] == SELECT:
            print(f"'{SELECT}' found")
            NEW_GRADE = input("New Grade: ")
            GRADE_ARRAY_2D[i][1] = NEW_GRADE
    
    GRADE_ARRAY_2D.append(NEW_GRADE)
    NEW_GRADE_TEXT = []

    for i in range(len(GRADE_ARRAY_2D)):
        NEW_GRADE_TEXT.append(GRADE_ARRAY_2D)

    GRADE_ARRAY = NEW_GRADE_TEXT

    return GRADE_ARRAY

def deleteGrade(GRADE_ARRAY):
    ''''''
    print(GRADE_ARRAY)
    
    GRADE_ARRAY_2D = []

    for i in range(len(GRADE_ARRAY)):
        GRADE_ARRAY_2D.append(GRADE_ARRAY[i].split())
    
    SELECT = input("Select subject: ")

    for i in range(len(GRADE_ARRAY_2D)):
        if GRADE_ARRAY_2D[i][0] == SELECT:
            print(f"'{SELECT}' found")
            NEW_GRADE = input("New Grade: ")
            GRADE_ARRAY_2D[i][1] = NEW_GRADE
    
    

### --- OUTPUT
def viewGrades(GRADES):
    ''''''
    print("Grades: ")
    for i in range(len(GRADES)):
        print(f"{GRADES[i]}")

def writeFile(GRADE_ARRAY):
    ''''''
    global FILENAME

    FILE = open(FILENAME, "w")
    GRADE_TEXT = ",".join(GRADE_ARRAY)
    FILE.write(GRADE_TEXT)
    FILE.close()
    print("Successfully saved grades")
### --- MAIN PROGRAM --- #

if __name__ == "__main__":
    FILE = getFileRead()
    GRADES = readFile(FILE)

    while True:
        CHOICE = menu()
        if CHOICE == 1:
            viewGrades(GRADES)
        elif CHOICE == 2:
            SUBJECT = getSubject()
            GRADE = getGrade()
            GRADES = addSubject(GRADE, SUBJECT, GRADES)
            writeFile(GRADES)
            pass
        elif CHOICE == 3:
            updateGrade(GRADES)
            pass
        elif CHOICE == 4:
            pass
        elif CHOICE == 5:
            pass
        elif CHOICE == 6:
            exit()