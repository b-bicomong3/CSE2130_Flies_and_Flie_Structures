#f_directory.py
'''
Title: Contacts Directory
Author: Beatrix Bicomng
Date: April 26, 2022
'''

import sqlite3
import sys
import pathlib

### --- VARIABLES --- ###
FILENAME = "f_directory.db"
FIRST_RUN = True

# Test if FILENAME already exists
if (pathlib.Path.cwd() / FILENAME).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(FILENAME)
CURSOR = CONNECTION.cursor()

### --- SUBROUTINES --- ###
## --- INPUT
def menu():
    """User selects how to interact with the contacts database

        Returns:
            CHOICE (int): user's selection
    """
    print('''
1. Search for contact  
2. View all contacts
3. Add contact
4. Edit contact
5. Delete contact
6. EXIT 
    ''')
    CHOICE = input("> ")

    try:
        CHOICE = int(CHOICE)
        return CHOICE
    except ValueError:
        print("Please enter a valid number")
        return menu()

def addContact():
    """User enter new contact information that is stores in the database

        Returns:
            None:
    """
    global CURSOR, CONNECTION
    # inputs
    FIRST_NAME = input("First Name: ")
    LAST_NAME = input("Last Name: ")
    EMAIL = input("Email: ")
    INSTAGRAM = input("Instagram: ")

    # processing 
    if FIRST_NAME == "" or LAST_NAME == "":
        print("Not enough information given")
    else:
        CURSOR.execute('''
            INSERT INTO
                contacts(
                    first_name,
                    last_name,
                    email,
                    instagram
                    )
                VALUES (
                    ?, ?, ?, ?
                    )
        ;''', (FIRST_NAME, LAST_NAME, EMAIL, INSTAGRAM))

    # output
    CONNECTION.commit()
    print(f"{FIRST_NAME} {LAST_NAME} successfully saved to contacts!")

def searchContactName():
    """Asks user for contact information to search for

    Returns:
        str: First name to be searched for
    """
    NAME = input("Name: ")
    return NAME

def getContactID():
    """Asks user to select contact

    Returns:
        int: primary key / contact id
    """
    global CURSOR

    CONTACTS = CURSOR.execute('''
        SELECT
            id,
            first_name,
            last_name
        FROM
            contacts
        ORDER BY
            first_name,
            last_name
    ;''').fetchall()

    print("Please select a contact")
    for i in range(len(CONTACTS)):
        print(f"{i+1}. {CONTACTS[i][1]} {CONTACTS[i][2]}")

    ROW_INDEX = input("> ")
    ROW_INDEX = int(ROW_INDEX) - 1

    CONTACT_ID = CONTACTS[ROW_INDEX][0]
    return CONTACT_ID

def updateContactID(ID):
    '''User updates contact information of contact ID :param ID: (int) primary key :return: (None)'''

    global CURSOR, CONNECTION

    CONTACT = CURSOR.execute('''
        SELECT
            first_name,
            last_name,
            email,
            instagram
        FROM
            contacts
        WHERE
            id = ?
    ;''', [ID]).fetchone()

    print("Leave field blank for no changes")

    # inputs
    FIRST_NAME = input(f"First Name: ({CONTACT[0]}) ")
    LAST_NAME = input(f"Last Name: ({CONTACT[1]}) ")
    EMAIL = input(f"Email: ({CONTACT[2]}) ")
    INSTA = input(f"Instagram: ({CONTACT[3]}) ")

    # processing
    INFO = (FIRST_NAME, LAST_NAME, EMAIL, INSTA)

    NEW_INFO = []

    for i in range(len(INFO)):
        if INFO[i] == "":
            NEW_INFO.append(CONTACT[i])
        else:
            NEW_INFO.append(INFO[i])

    NEW_INFO.append(ID)

    # outputs
    CURSOR.execute('''
        UPDATE
            contacts
        SET
            first_name = ?,
            last_name = ?,
            email = ?,
            instagram = ?
        WHERE
            id = ?

    ;''', NEW_INFO)

    CONNECTION.commit()
    print(f"{CONTACT[0]} {CONTACT[1]} has been updated")

### --- PROCESSING --- ###
def setup():
    """Creates contact table if it does not exist

    Returns:
        None: 
    """
    global CURSOR, CONNECTION
    CURSOR.execute('''
        CREATE TABLE contacts(
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            instagram TEXT
        )
    ;''')

    CONNECTION.commit()

def queryContactName(NAME):
    """Queries the database and returns a 2D array of results

    Args:
        NAME (str): 

    Returns:
        list: 2D array pf results
    """
    global CURSOR
    RESULTS = CURSOR.execute('''
        SELECT
            first_name,
            last_name,
            email,
            instagram
        FROM
            contacts
        WHERE
            first_name = ?
        ORDER BY
            last_name
    ;''', [NAME]).fetchall()

    return RESULTS

def deleteContact(ID):
    '''Delete a contact from the contacts database :param ID: (int) primary key :return: (None)'''
    global CURSOR, CONNECTION

    CONTACT = CURSOR.execute('''
        SELECT
            first_name,
            last_name
        FROM
            contacts
        WHERE
            id = ?
    ;''', [ID]).fetchone()

    # DELETE
    CURSOR.execute('''
        DELETE FROM
            contacts
        WHERE
            id = ?
    ;''', [ID])

    CONNECTION.commit()

    print("%s %s successfully deleted" % CONTACT)

### --- OUTPUTS --- ###
def dispResults(RESULTS):
    """Displays the search results for the user

    Args:
        RESULTS (list): 2D array of results

    Returns:
        None: 
    """
    for i in range(len(RESULTS)):
        print("%s %s (email: %s) (insta: %s)" % RESULTS[i])

def dispALLContacts():
    """Displays all contacts alphabetically by first name

        Returns:
            None:
    """
    CONTACTS = CURSOR.execute('''
        SELECT
            first_name,
            last_name
        FROM
            contacts
        ORDER BY
            first_name
    ;''').fetchall()

    for i in range(len(CONTACTS)):
        print(f"{CONTACTS[i][0]} {CONTACTS[i][1]}")
# print(f"{CONTACTS[i][0]} {CONTACTS[i][1]}") prints the first
# name [0] from the first row of the table [i], then the
# last name [1] from the first row of the table [i], then moves
# to the next row of the table (next value of [i])

### --- MAIN PROGRAM --- ###
if __name__ == "__main__":
    if FIRST_RUN:
        setup()

    while True:
        CHOICE = menu()
        if CHOICE == 1:
            SEARCH_NAME = searchContactName()
            SEARCH_RESULTS = queryContactName(SEARCH_NAME)
            dispResults(SEARCH_RESULTS)
        elif CHOICE == 2:
            dispALLContacts()
        elif CHOICE == 3:
            addContact()
        elif CHOICE == 4:
            ID = getContactID()
            updateContactID(ID)
        elif CHOICE == 5:
            ID = getContactID()
            deleteContact(ID)
        else:
            exit()