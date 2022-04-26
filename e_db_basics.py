#e_db_basics.py
'''
Title: Database basics
Author: Beatrix Bicomong
Date: April 25, 2022
'''

import sqlite3

### -- VARIABLES --- ###
FILENAME = "f_contacts.db"

CONNECTION = sqlite3.connect(FILENAME)
CURSOR = CONNECTION.cursor()
#CURSOR is the object that writes SQL commands

# Create the database table
CURSOR.execute('''
    CREATE TABLE
        contacts(
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT
        )
;''')

CONNECTION.commit()
# verifies and saves any uncommited information

# Create a row of data into the table
CURSOR.execute('''
    INSERT INTO
        contacts
    VALUES(
        1,
        "Beatrix",
        "Bicomong",
        "b.bicomong@share.epsb.ca"

    )
''')

CONNECTION.commit()