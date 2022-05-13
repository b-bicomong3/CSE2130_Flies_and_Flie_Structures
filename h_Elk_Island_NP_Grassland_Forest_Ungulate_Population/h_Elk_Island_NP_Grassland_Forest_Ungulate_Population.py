#h_Elk_Island_NP_Grassland_Forest_Ungulate_Population
'''
Title: Elk Island NP Grassland Forest Ungulate Population
Author: Beatrix Bicomong
Date: May 05, 2022
'''

import sys
import pathlib
import sqlite3

### --- VARIBLES -- ###

ELK_FILE = "Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv"
DATABASE_FILE = "elk_island.db"

FIRST_RUN = True

if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

ANIMALS = {
    1 : "Bison",
    2 : "Elk",
    3 : "Moose",
    4 : "Deer",
}

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
3. Delete current data
4. Exit
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

    RAW_DATA.pop(0)

    CURSOR.execute('''
        CREATE TABLE
            elk_island(
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
                Fall_population_estimate INTEGER NOT NULL,
                Survey_comment TEXT,
                Estimate_method TEXT,

                PRIMARY KEY(Area_of_park, Population_year, Species_name)
                )
    ;''')
    
    CONNECTION.commit()

    for i in range(len(RAW_DATA)):
        CURSOR.execute('''
            INSERT INTO
                elk_island
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ;''', RAW_DATA[i])

    CONNECTION.commit()
    print("Successfully loaded all data!")


def askYear():
    ''''''
    global CURSOR, ANIMALS
    
    # inputs
    START = input("Start year? ")
    START = int(START)
    END = input("End year? ")
    END= int(END)
    ANIMAL = input("Bison (1), Elk (2), Moose (3), Deer (4), or All (5) ")

    ANIMAL = int(ANIMAL)   
    if ANIMAL == 5:
        return animalMult(START, END)
    else:    
        ANIMAL = ANIMALS[ANIMAL]

    # processing 
    YEAR_START_N = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Species_name = ? and
            Area_of_park = "North"
        ORDER BY
            Species_name

    ;''', [START, ANIMAL]).fetchall()

    YEAR_END_N = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Species_name = ? and
            Area_of_park = "North"
        ORDER BY
            Species_name
    ;''', [END, ANIMAL]).fetchall()

    YEAR_START_S = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Species_name = ? and
            Area_of_park = "South"
        ORDER BY
            Species_name

    ;''', [START, ANIMAL]).fetchall()

    YEAR_END_S = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Species_name = ? and
            Area_of_park = "South"
        ORDER BY
            Species_name
    ;''', [END, ANIMAL]).fetchall()

    EMPTY = []

    # outputs 
    if YEAR_END_N == list(EMPTY) or YEAR_END_S == list(EMPTY) or END != YEAR_END_N[0][1] or END != YEAR_END_S[0][1]:
        print("One of the inputted years does not exist in our database, re-enter year or add year to data")
        print("Please make sure both North and South areas are available from that year")
        print('''
    1. Re-enter year
    2. Add year
        ''')
        CHOICE= input("> ")
        CHOICE = int(CHOICE)
        if CHOICE == 1:
            return askYear()
        elif CHOICE == 2:
            return addData()

    if "North" != YEAR_START_N[0][0] or "North" not in YEAR_END_N[0][0]:
        YEAR_START_N = 0
        YEAR_END_N = 0

    if "South" not in YEAR_START_S[0][0] or "South" not in YEAR_END_S[0][0]:
        YEAR_START_S = 0
        YEAR_END_S = 0

    return YEAR_START_N, YEAR_END_N, YEAR_START_S, YEAR_END_S

def animalMult(START, END):
    ''''''

    YEAR_START_N = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Area_of_park = "North"
        ORDER BY
            Species_name

    ;''', [START]).fetchall()

    YEAR_END_N = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Area_of_park = "North"
        ORDER BY
            Species_name
    ;''', [END]).fetchall()

    YEAR_START_S = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Area_of_park = "South"
        ORDER BY
            Species_name

    ;''', [START]).fetchall()

    YEAR_END_S = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Area_of_park = "South"
        ORDER BY
            Species_name
    ;''', [END]).fetchall()

    EMPTY = []

    # outputs 

    if "North" != YEAR_START_N[0][0] or "North" not in YEAR_END_N[0][0]:
        YEAR_START_N = 0
        YEAR_END_N = 0

    if "South" not in YEAR_START_S[0][0] or "South" not in YEAR_END_S[0][0]:
        YEAR_START_S = 0
        YEAR_END_S = 0

    if YEAR_END_N == list(EMPTY) or YEAR_END_S == list(EMPTY) or END != YEAR_END_N[0][1] or END != YEAR_END_S[0][1]:
        print(f"One of the inputted years does not exist in our database, re-enter year or add year to data")
        print('''
    1. Re-enter year
    2. Add year
        ''')
        CHOICE= input("> ")
        CHOICE = int(CHOICE)
        if CHOICE == 1:
            return askYear()
        elif CHOICE == 2:
            return addData()

    return YEAR_START_N, YEAR_END_N, YEAR_START_S, YEAR_END_S

def addData():
    ''''''
    global CURSOR, CONNECTION

    # inputs
    AREA_OF_PARK = input("Area of park: ")
    POPULATION_YEAR = input("Population year: ")
    SURVEY_YEAR = input("Survey Year: ")
    SURVEY_MONTH = input("Survey Month: ")
    SURVEY_DAY = input("Survey Day: ")
    SPECIES_NAME = input("Species name: ")
    UNKNOWN_AGE_AND_SEX_COUNT = input("Unknown age and sex count: ")
    ADULT_MALE_COUNT = input("Adult male count: ")
    ADULT_FEMALE_COUNT = input("Adult female count: ")
    ADULT_UNKNOWN_COUNT = input("Adult unknown count: ")
    YEARLING_COUNT = input("Yearling count: ")
    CALF_COUNT = input("Calf count: ")
    SURVEY_TOTAL = input("Survey Total: ") 
    SIGHTIBILTY_CORRECTION_FACTOR = input("Sightibility correction factor: ")
    ADDITIONAL_CAPTIVE_COUNT = input("Additional captive count: ")
    ANIMALS_REMOVED_PRIOR_TO_SURVEY = input("Animals removed prior to suvrey: ")
    FALL_POPULATION_ESTIMATE = input("Fall population estimate: ")
    SURVEY_COMMENT = input("Survey comment: ")
    ESTIMATE_METHOD= input("Estimate method: ")

    # processing 
    if AREA_OF_PARK == "" or POPULATION_YEAR == "" or SPECIES_NAME == "" or FALL_POPULATION_ESTIMATE == "":
        print("Not enough information given")
    else:
        CURSOR.execute('''
            INSERT INTO
                elk_island(
                    Area_of_park,
                    Population_year,
                    Survey_Year,
                    Survey_Month,
                    Survey_Day,
                    Species_name,
                    Unknown_age_and_sex_count,
                    Adult_male_count,
                    Adult_female_count,
                    Adult_unknown_count,
                    Yearling_count,
                    Calf_count,
                    Survey_total,
                    Sightability_correction_factor,
                    Additional_captive_count,
                    Animals_removed_prior_to_survey,
                    Fall_population_estimate,
                    Survey_comment,
                    Estimate_method
                    )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
        ;''', (AREA_OF_PARK, POPULATION_YEAR, SURVEY_YEAR, SURVEY_MONTH, SURVEY_DAY, SPECIES_NAME, 
        UNKNOWN_AGE_AND_SEX_COUNT, ADULT_MALE_COUNT, ADULT_FEMALE_COUNT, ADULT_UNKNOWN_COUNT, YEARLING_COUNT,
        CALF_COUNT, SURVEY_TOTAL, SIGHTIBILTY_CORRECTION_FACTOR, ADDITIONAL_CAPTIVE_COUNT, 
        ANIMALS_REMOVED_PRIOR_TO_SURVEY, FALL_POPULATION_ESTIMATE, SURVEY_COMMENT, ESTIMATE_METHOD))

    # output
    CONNECTION.commit()
    print(f"Year {POPULATION_YEAR} successfully saved to contacts!")

    return askYear()

def getDataID():
    ''''''
    global CURSOR

    DATA = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        ORDER BY
            Population_year,
            Species_name
    ;''').fetchall()
    print("Please select a contact")
    for i in range(len(DATA)):
        print(f"> {DATA[i][0]} {DATA[i][1]} {DATA[i][2]} {DATA[i][3]}")

    print("Please enter the area, year and animal of data: ")

    AREA_ID = input("Area: ")
    YEAR_INDEX = input("Year: ")
    YEAR_ID = int(YEAR_INDEX)
    ANIMAL_ID = input("Animal: ")

    return AREA_ID, YEAR_ID, ANIMAL_ID

### --- PROCESSINGS

def calcPopulation(YEAR_START_N, YEAR_END_N, YEAR_START_S, YEAR_END_S):
    ''''''
    if len(YEAR_START_N) == 4:
        NUMBER_1_N = []
        NUMBER_2_N = []
        NUMBER_1_S = []
        NUMBER_2_S = []
        for i in range(len(YEAR_START_N)):
            NUMBER_1_N.append(YEAR_START_N[i][3])
        for i in range(len(YEAR_END_N)):
            NUMBER_2_N.append(YEAR_END_N[i][3])
        for i in range(len(YEAR_START_S)):
            NUMBER_1_S.append(YEAR_START_S[i][3])
        for i in range(len(YEAR_END_S)):
            NUMBER_2_S.append(YEAR_END_S[i][3])
    elif YEAR_START_N == 0 and YEAR_END_N == 0:
        NUMBER_1_N = 0
        NUMBER_2_N = 0
        NUMBER_1_S = YEAR_START_S[0][3]
        NUMBER_2_S = YEAR_END_S[0][3]
    elif YEAR_START_S == 0 and YEAR_END_S == 0:
        NUMBER_1_N = YEAR_START_N[0][3]
        NUMBER_2_N = YEAR_END_N[0][3]
        NUMBER_1_S = 0
        NUMBER_2_S = 0
    else:
        NUMBER_1_N = YEAR_START_N[0][3]
        NUMBER_2_N = YEAR_END_N[0][3]
        NUMBER_1_S = YEAR_START_S[0][3]
        NUMBER_2_S = YEAR_END_S[0][3]

    NUMBER_YEAR_1 = YEAR_START_N[0][1]
    NUMBER_YEAR_2 = YEAR_END_N[0][1]

    if len(YEAR_START_N) == 4:
        CALC_B_1 = NUMBER_2_N[0] + NUMBER_2_S[0]
        CALC_E_1 = NUMBER_2_N[2] + NUMBER_2_S[2]
        CALC_M_1 = NUMBER_2_N[3] + NUMBER_2_S[3]
        CALC_D_1 = NUMBER_2_N[1] + NUMBER_2_S[1]

        CALC_B_2 = NUMBER_1_N[0] + NUMBER_1_S[0]
        CALC_E_2 = NUMBER_1_N[2] + NUMBER_1_S[2]
        CALC_M_2 = NUMBER_1_N[3] + NUMBER_1_S[3]
        CALC_D_2 = NUMBER_1_N[1] + NUMBER_1_S[1]

        CALC_B_3 = CALC_B_1 - CALC_B_2
        CALC_E_3 = CALC_E_1 - CALC_E_2
        CALC_M_3 = CALC_M_1 - CALC_M_2
        CALC_D_3 = CALC_D_1 - CALC_D_2

        CALC_YEAR = NUMBER_YEAR_2 - NUMBER_YEAR_1

        SUM_B = CALC_B_3 / CALC_YEAR
        SUM_E = CALC_E_3 / CALC_YEAR
        SUM_M = CALC_M_3 / CALC_YEAR
        SUM_D = CALC_D_3 / CALC_YEAR

        SUM_B = round(SUM_B)
        SUM_E = round(SUM_E)
        SUM_M = round(SUM_M)
        SUM_D = round(SUM_D)

        SUM_ANIMAL_B = YEAR_START_N[0][2]
        SUM_ANIMAL_E = YEAR_START_N[2][2]
        SUM_ANIMAL_M = YEAR_START_N[3][2]
        SUM_ANIMAL_D = YEAR_START_N[1][2]

        SUM = SUM_B, SUM_E, SUM_M, SUM_D
        SUM_ANIMAL = SUM_ANIMAL_B, SUM_ANIMAL_E, SUM_ANIMAL_M, SUM_ANIMAL_D

        return dispAll(SUM, SUM_ANIMAL)
    else:
        CALC_1 = NUMBER_2_N + NUMBER_2_S
        CALC_2 = NUMBER_1_N + NUMBER_1_S

        CALC_3 = CALC_1 - CALC_2

        CALC_YEAR = NUMBER_YEAR_2 - NUMBER_YEAR_1

        SUM = CALC_3 / CALC_YEAR

        SUM = round(SUM)

        SUM_ANIMAL = YEAR_START_N[0][2]

    return SUM, SUM_ANIMAL


def deleteData(AREA_ID, YEAR_ID, ANIMAL_ID):
    ''''''
    global CURSOR, CONNECTION

    DELETE = CURSOR.execute('''
        SELECT
            Area_of_park,
            Population_year,
            Species_name,
            Fall_population_estimate
        FROM 
            elk_island
        WHERE
            Population_year = ? and
            Species_name = ? and
            Area_of_park = ?
    ;''', [AREA_ID, YEAR_ID, ANIMAL_ID]).fetchone()

    # DELETE
    CURSOR.execute('''
        DELETE FROM
            elk_island
        WHERE
            Area_of_park = ? and
            Population_year = ? and
            Species_name = ?
    ;''', [AREA_ID, YEAR_ID, ANIMAL_ID])

    CONNECTION.commit()

    print("%s %s %s %s successfully deleted" % DELETE)

### --- OUTPUTS

def diplayResult(SUM, SUM_ANIMAL):
    ''''''
    print(f"{SUM} {SUM_ANIMAL}/yr")
    
def dispAll(SUM, SUM_ANIMAL):
    ''''''
    for i in range(len(SUM)):
        print(f"{SUM[i]} {SUM_ANIMAL[i]}/yr")

    return menu()

### --- MAIN PROGRAM --- ###

if __name__ == "__main__":
    intro()
    if FIRST_RUN:
        ELK = getRawData(ELK_FILE)
        importElk(ELK)
    while True:
        CHOICE = menu()
        if CHOICE == 1:
            DATA_1, DATA_2, DATA_3, DATA_4 = askYear()
            RESULT, RESULT_ANIMAL = calcPopulation(DATA_1, DATA_2, DATA_3, DATA_4)
            diplayResult(RESULT, RESULT_ANIMAL)
        elif CHOICE == 2:
            addData()
        elif CHOICE == 3:
            AREA_ID, YEAR_ID, ANIMAL_ID = getDataID()
            deleteData(AREA_ID, YEAR_ID, ANIMAL_ID)
        elif CHOICE == 4:
            exit
        else:
            pass
