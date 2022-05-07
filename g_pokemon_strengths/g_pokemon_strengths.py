#g_pokemon_strengths.py
'''
Title: Pokemon Strengths
Author: Beatrix Bicomong
Date: April 28, 2022
'''

import sys
import pathlib
import sqlite3

### --- VARIABLES --- ###
POKEMON_FILE = "pokemon.csv"
STRENGTH_FILE = "pokemon_type_strong.csv"
DATABASE_FILE = "pokemon.db"

FIRST_RUN = True

if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

### --- SUBROUTINES --- ###

### --- INPUTS
def menu():
    """User selects program action

    Returns:
        int:
    """
    print('''
1. View a pokemon's type advantage
2. View which types are weak against a type (attack is super effective!)
3. View which types are strong against a type (attack is not very effective)
    ''')

    CHOICE = input("> ")
    CHOICE = int(CHOICE)

    return CHOICE 

def getRawData(FILENAME):
    """Reads CSV File and extracts unprocessed data

    Args:
        FILENAME (str): 

    Returns:
        list: 2D array of data
    """
    FILE = open(FILENAME)
    CONTENT = FILE.readlines()
    FILE.close()

    for i in range(len(CONTENT)):
        CONTENT[i] = CONTENT[i].rstrip() ## removes \n at the end of the line
        CONTENT[i] = CONTENT[i].split(",") # splitting string into list

    return CONTENT

def importPokemon(RAW_DATA):
    """Import data into the database

    Args:
        RAW_DATA (list): 2D list

    Returns:
        None: 
    """
    global CURSOR, CONNECTION

    # remove all MEGA pokemon rows
    for i in range(len(RAW_DATA)-2,-1,-1):
        if RAW_DATA[i][0] == RAW_DATA[i+1][0]:
            RAW_DATA.pop(i+1)

    # lowercase all types
    for i in range(len(RAW_DATA)):
        RAW_DATA[i][2] = RAW_DATA[i][2].lower() # lowercase type 1
        RAW_DATA[i][3] = RAW_DATA[i][3].lower() # lowercase type 2

    RAW_DATA.pop(0)

    # create table on database

    CURSOR.execute('''
        CREATE TABLE
            pokemon(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type_1 TEXT NOT NULL, 
                type_2 TEXT
                )
    ;''')

    CONNECTION.commit()

    for i in range(len(RAW_DATA)):
        CURSOR.execute('''
            INSERT INTO
                pokemon
            VALUES (
                ?, ?, ?, ?
            )
        ;''', RAW_DATA[i][:4])

    CONNECTION.commit()
    print("Successfully loaded all pokemon names and types!")

def importStrength(RAW_DATA):
    """Load and import pokemon strengths

    Args:
        RAW_DATA (list): 2D array
    Returns:
        None:
    """    
    global CURSOR, CONNECTION

    for i in range(len(RAW_DATA)):
        for j in range(len(RAW_DATA[i])):
            if RAW_DATA[i][j] == "":
                RAW_DATA[i][j] = None

    RAW_DATA.pop(0)

    CURSOR.execute('''
        CREATE TABLE
            strong(
                type TEXT PRIMARY KEY,
                type_1 TEXT,
                type_2 TEXT,
                type_3 TEXT,
                type_4 TEXT,
                type_5 TEXT
            )
    ;''')

    CONNECTION.commit()

    for i in range(len(RAW_DATA)):
        CURSOR.execute('''
            INSERT INTO
                strong
            VALUES (
                ?, ?, ?, ?, ?, ?
            )
    ;''', RAW_DATA[i])

    CONNECTION.commit()
    print("Successfully loaded all pokemon strengths!")
    # may need to specifiy that al type_x are TEXT

def askPokemon():
    '''Ask for pokemon name :return: (str)'''

    NAME = input("Pokemon: ")

    global CURSOR, CONNECTION

    POKEMON = CURSOR.execute('''
        SELECT
            id,
            name,
            type_1,
            type_2
        FROM 
            pokemon
        WHERE
            name = ?
    ;''', [NAME]).fetchall()
    POKEMON = POKEMON[0]
    return POKEMON

### --- PROCESSING
def getPokemonStrengths(POKEMON):
    '''Queries the database for the Pokemon type strengths :param POKEMON: (str) :return: (list) list of types pokemon is strong against'''
    
    global CURSOR
    RESULTS = CURSOR.execute('''
        SELECT
            type,
            type_1,
            type_2,
            type_3,
            type_4,
            type_5
        FROM
            strong
        WHERE
            type = ?
    ;''', [POKEMON]).fetchall()

    return RESULTS

    # get strengths for both types if a pokemon has 2 types
    
    #return RESULTS

### --- OUTPUTS
def dispPokemonStrengths(NAME, RESULTS):
    '''displays types a pokemon is strong against :param NAME: (str) :param RESULTS: (list) :return: (None)'''
    

### --- MAIN PROGRAM --- ###

if __name__ == "__main__":
    if FIRST_RUN:
        POKEMON = getRawData(POKEMON_FILE)
        STRENGTHS = getRawData(STRENGTH_FILE)
        importPokemon(POKEMON)
        importStrength(STRENGTHS)
        NAME = askPokemon()
        print(NAME)
        TYPES = getPokemonStrengths(NAME)
        print(TYPES)

    # NAME = askPokemon()
    # 
    # dispPokemonStrengths(NAME, TYPES)