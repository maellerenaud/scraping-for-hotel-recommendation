import sqlite3

from utils import *

def connection(town, arrival_date, departure_date):
    adapted_town_name = convert_string_to_file_name(town)
    db_name = "{}-{}-{}".format(adapted_town_name, arrival_date, departure_date)
    conn = sqlite3.connect('{}.db'.format(db_name,))
    return conn

def create_tables(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS Results
                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    hotelName VARCHAR(255) NOT NULL,
                    comparator VARCHAR(15),
                    price INT,
                    grade FLOAT,
                    nbVotes INT,
                    address VARCHAR(255),
                    distance FLOAT,
                    wifi BIT,
                    minibar BIT,
                    clim BIT);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS Points
                    (hotelName VARCHAR(255) PRIMARY KEY,
                    pricePoints FLOAT,
                    gradePoints FLOAT,
                    distancePoints FLOAT,
                    wifiPoints FLOAT,
                    minibarPoints FLOAT,
                    climPoints FLOAT,
                    rankingScore FLOAT);''')
    conn.commit()

