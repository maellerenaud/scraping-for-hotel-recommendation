from manage_database import *
from tripadvisor import *

def find_best_hotel(town, arrival_date, departure_date):
    conn = connection(town, arrival_date, departure_date)
    create_tables(conn)
    browser = setup_browser(r"../chromedriver")
    request(browser, town, arrival_date, departure_date)
    visit_hotels_all_pages(conn, browser)
    fill_distances(conn, town)
    fill_points_table(conn)
    return ranking_all_hotels(conn)
