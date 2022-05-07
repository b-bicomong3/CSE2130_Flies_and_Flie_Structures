#h_Elk_Island_NP_Grassland_Forest_Ungulate_Population
'''
Title: Elk Island NP Grassland Forest Ungulate Population
Author: Beatrix Bicomong
Date: May 05, 2022
'''
import sys
import pathlib
import sqlite3

ELK_FILE = "Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv"
DATABASE_FILE = "Elk_Island.db"

FIRST_RUN = True

if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

### --- SUBROUTINES --- ###
def intro():
    ''''''
    print("Welcome to the Elk Island National Park Large Mammal population database!")
### --- INPUTS
def menu():
    """User selects program action

    Returns:
        int:
    """
    print("Please choose an option: ")
    print('''
1. Search Population Growth
2. Add new year data
3. Exit
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
        CONTENT[i] = CONTENT[i].rstrip() # removes \n at the end of the line
        
        CONTENT[i] = CONTENT[i].split(",") # splitting string into list

    return CONTENT

def importElk(RAW_DATA):
    ''''''
    global CURSOR, CONNECTION

    CURSOR.execute('''
        CREATE TABLE
            elk_island(
                id INTEGER PRIMARY KEY,
                Area_of_park TEXT NOT NULL,
                Population_year INTEGER NOT NULL,
                Survey_Year TEXT,
                Survey_Month TEXT,
                Survey_Day TEXT,
                Species_name TEXT NOT NULL,
                Unknown_age_and_sex_count TEXT,
                Adult_male_count TEXT,
                Adult_female_count TEXT,
                Adult_unknown_count TEXT,
                Yearling_count TEXT,
                Calf_count TEXT,
                Survey_total TEXT,
                Sightability_correction_factor TEXT,
                Additional_captive_count TEXT,
                Animals_removed_prior_to_survey TEXT,
                Fall_population_estimate TEXT,
                Survey_comment TEXT,
                Estimate_method TEXT
                )
    ;''')
    
    CONNECTION.commit()

    for i in range(len(RAW_DATA)):
        CURSOR.execute('''
            INSERT INTO
                elk_island
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ;''', RAW_DATA[i])

    CONNECTION.commit()
    print("Successfully loaded all data!")

### --- PROCESSINGS

### --- OUTPUTS

### --- MAIN PROGRAM --- ###

if __name__ == "__main__":
    intro()
    if FIRST_RUN:
        ELK = getRawData(ELK_FILE)
        importElk(ELK)
        CHOICE = menu()
        if CHOICE == 1:
            pass
        if CHOICE == 2:
            pass
        else:
            exit()