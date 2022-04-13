# b_highscore.py

'''
Title: High Score Tracker
Author: Beatrix Bicomong
Date: April 12, 2022
'''

### --- VARIBALES --- ###
FILENAME = "b_score.txt"

### --- INPUT
def getFileRead():
    """_summary_

    Returns:
        str: FILE
    """

    global FILENAME
    try:
        FILE = open(FILENAME, "x")
        START_SCORE = []
        for i in range(10):
            START_SCORE.append("AAA 0")
        START_SCORE_TEXT = ",".join(START_SCORE)
        FILE.write(START_SCORE_TEXT)
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
1. View Score    
2. Add New Score    
3. Exit    
    """)

    CHOICE = input("> ")

    if CHOICE.isnumeric():
        CHOICE = int(CHOICE)
    else:
        print("Please enter a number!")

        return menu()
    if 0 < CHOICE < 4:

        return CHOICE
    else:
        print("Please enter a number in the menu")

        return menu()

def getScore():
    """Get the player's score

    Returns:
        SCORE (int): 
    """

    SCORE = input("Score: ")

    if SCORE.isnumeric():
        return int(SCORE)
    else:
        print("Please enter a number")
        return getScore()

def getName():
    """Asks user for their name

    Returns:
        NAME (str): 
    """

    NAME = input("Name: ")
    NAME = NAME.upper()
    if len(NAME) > 3:
        NAME = NAME[:3]
    
    return NAME


### --- PROCESSING
def readFile(FILE_OBJ):
    """Reading the contents of the file

    Args:
        FILE_OBJ (object): 

    Returns:
        SCORE_ARRAY (list):
    """

    TEXT = FILE_OBJ.read()
    FILE_OBJ.close()
    SCORE_ARRAY = TEXT.split(",")

    return SCORE_ARRAY

def checkNewScore(SCORE, SCORE_ARRAY):
    """Tests whether the new score is a high score

    Args:
        SCORE (int): 
        SCOREARRAY (list): 
    
    Return:
        bool:
    """

    SCORE_ARRAY_2D = []
    # Creates a 2D array with the scores set a integers
    for i in range(len(SCORE_ARRAY)):
        SCORE_ARRAY_2D.append(SCORE_ARRAY[i].split())
        SCORE_ARRAY_2D[-1][1] = int(SCORE_ARRAY_2D[-1][1])
    
    for i in range(len(SCORE_ARRAY_2D)):
        if SCORE >= SCORE_ARRAY_2D[i][1]:
            return True
    return False

def updateHighScore(SCORE, NAME, SCORE_ARRAY):
    """Updates the score list with a name score

    Args:
        SCORE (int): 
        NAME (str): 
        SCORE_ARRAY (list): 

    Return:
        SCORE_ARRAY (list):
    """

    SCORE_ARRAY_2D = []
    # Creates a 2D array with the scores set a integers
    for i in range(len(SCORE_ARRAY)):
        SCORE_ARRAY_2D.append(SCORE_ARRAY[i].split())
        SCORE_ARRAY_2D[-1][1] = int(SCORE_ARRAY_2D[-1][1])

    for i in range(len(SCORE_ARRAY)):
        if SCORE > SCORE_ARRAY_2D[i][1]:
            SCORE_ARRAY.insert(i, f"{NAME} {SCORE}")
            SCORE_ARRAY.pop()

            return SCORE_ARRAY

### --- OUTPUTS
def viewScores(SCORES):
    """Displays the scores nicely

    Args:
        SCORES (list):
    """

    print("HIGH SCORES!")
    for i in range(len(SCORES)):
        print(f"{i+1}. {SCORES[i]}")

def writeFile(SCORE_ARRAY):
    """Writes the changes to th file

    Args:
        SCORE_ARRAY (list):
    """

    global FILENAME

    FILE = open(FILENAME, "w")
    SCORE_TEXT = ",".join(SCORE_ARRAY)
    FILE.write(SCORE_TEXT)
    FILE.close()
    print("Successfully saved High Scores!")

### --- MAIN PROGRAM --- ###

if __name__ == "__main__":

    FILE = getFileRead()
    SCORES = readFile(FILE)
    
    while True:
        CHOICE = menu()
        if CHOICE == 1:
            viewScores(SCORES)
        elif CHOICE == 2:
            SCORE = getScore()
            if checkNewScore(SCORE, SCORES):
                print("High Score!")
                NAME = getName()
                SCORES = updateHighScore(SCORE, NAME, SCORES)
                writeFile(SCORES)
            else:
                print("Score is not high enough...")
        elif CHOICE == 3:
            exit()