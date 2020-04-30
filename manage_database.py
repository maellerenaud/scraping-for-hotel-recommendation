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
                    comparator VARCHAR(15) NOT NULL,
                    price INT NOT NULL,
                    grade FLOAT,
                    nbVotes INT,
                    address VARCHAR(255) NOT NULL,
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

def save(conn, hotel_name, comparator, price, grade, nb_votes, address, distance, wifi, minibar, clim):
    hotel_name = normalize_string(hotel_name)
    address = normalize_string(address)
    conn.execute('''INSERT INTO Results 
                    (hotelName, comparator, price, grade, nbVotes, address, distance, wifi, minibar, clim)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (hotel_name, comparator, price, grade, nb_votes, address, distance, wifi, minibar, clim))
    conn.commit()

def fill_distances(conn, town):
    cursor = conn.execute(''' SELECT id, address
                              FROM Results
                              WHERE distance IS NULL''')
    for row in cursor:
        id, address = row
        distance = get_distance(town, address)
        conn.execute('UPDATE Results set distance = ? WHERE id = ?', (distance, id))
    conn.commit()
