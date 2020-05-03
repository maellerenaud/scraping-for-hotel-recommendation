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
    cursor = conn.execute(''' SELECT id, address, hotelName
                              FROM Results
                              WHERE distance IS NULL''')
    for row in cursor:
        id, address, hotel_name = row
        distance = get_distance(town, hotel_name, address)
        conn.execute('UPDATE Results set distance = ? WHERE id = ?', (distance, id))
    conn.commit()

def fill_points_table(conn):
    cursor = conn.execute('''SELECT MIN(bestPrice), MAX(bestPrice), MIN(bestGrade), MAX(bestGrade), MIN(bestDistance), MAX(bestDistance)
                             FROM (SELECT MIN(price) as bestPrice, AVG(grade) as bestGrade, MIN(distance) as bestDistance
                                   FROM Results
                                   GROUP BY hotelName)''')
    price_min, price_max, grade_min, grade_max, distance_min, distance_max = cursor.fetchone()
    cursor = conn.execute('''SELECT hotelName, MIN(price), AVG(grade), SUM(nbVotes), MIN(distance),
                                CAST(MAX(CAST(wifi as INT)) AS BIT), CAST(MAX(CAST(minibar as INT)) AS BIT), CAST(MAX(CAST(clim as INT)) AS BIT)
                             FROM Results
                             GROUP BY hotelName''')
    for row in cursor:
        hotel_name, price, grade, nb_votes, distance, wifi, minibar, clim = row
        pts_price = points_price(price, price_min, price_max)
        pts_grade = points_grade(grade, grade_min, grade_max)
        pts_distance = points_distance(distance, distance_min, distance_max)
        pts_wifi = points_wifi(wifi)
        pts_minibar = points_minibar(minibar)
        pts_clim = points_clim(clim)
        score = ranking_score(price, price_min, price_max, grade, grade_min, grade_max, distance, distance_min, distance_max, wifi, minibar, clim)
        conn.execute('''INSERT INTO Points
                        (hotelName, pricePoints, gradePoints, distancePoints, wifiPoints, minibarPoints, climPoints, rankingScore)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (hotel_name, pts_price, pts_grade, pts_distance, pts_wifi, pts_minibar, pts_clim, score))
    conn.commit()

def hotel_with_best_score(conn):
    cursor = conn.execute('''SELECT hotelName
                             FROM Points
                             ORDER BY rankingScore DESC
                             LIMIT 1''')
    best_hotel = cursor.fetchone()[0]
    return best_hotel

def ranking_all_hotels(conn):
    cursor = conn.execute('''SELECT hotelName, rankingScore
                             FROM Points
                             ORDER BY rankingScore DESC''')
    return cursor.fetchall()
