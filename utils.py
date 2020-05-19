from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
from datetime import date, datetime

### Set up browser

def setup_browser(path_chromedriver):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximised") #"kiosk" sur mac
    prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
    option.add_experimental_option('prefs', prefs)
    browser = webdriver.Chrome(executable_path=path_chromedriver, options=option)
    return browser

### Utils to fill database

def convert_string_to_file_name(string):
    lower_case = string.lower()
    return lower_case.replace(' ', '-')

def normalize_string(string):
    lower_case = string.lower()
    lower_case = lower_case.replace(' - ', ' ')
    lower_case = lower_case.replace(',', '')
    return lower_case

def convert_distance_string_into_float(string):
    '''from string distance with unit, return float distance in km'''
    distance_with_unit = string.split(' ')
    distance_string = distance_with_unit[0].split(',')
    if len(distance_string) > 1:
        distance = int(distance_string[0]) + 0.1 * int(distance_string[1])
    else:
        distance = int(distance_string[0])
    if distance_with_unit[1] == 'm':
        return distance / 1000
    return distance

def get_distance(town, hotel_name, address):
    browser = setup_browser(r"./chromedriver")
    town_url = "{}+office+de+tourisme".format(town,)
    address_url = '+'.join(hotel_name.split(' ')) + '+' + '+'.join(address.split(' '))
    url = "https://www.google.fr/maps/dir/{}/{}/".format(address_url, town_url)
    print(url)
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    button_car = wait.until(ec.presence_of_element_located((By.XPATH, '//button/div[@aria-label="Voiture"]')))
    button_car.click()
    wait = WebDriverWait(browser, 10)
    distance = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@id="section-directions-trip-0"]/div[2]/div[1]/div[1]/div[2]/div[1]'))).text
    browser.close()
    return convert_distance_string_into_float(distance)

### Attribute points to each criteria to get a ranking function on 100 points

points_sharing = {'price': 30, 'grade': 20, 'distance': 20, 'wifi': 15, 'minibar': 5, 'clim': 10}

def points_price(price, price_min, price_max):
    if price_min == price_max:
        return points_sharing['price']
    slices = [price_min + (price_max - price_min) * k / 10 for k in range(11)]
    slice_indice = 0
    while slices[slice_indice + 1] < price:
        slice_indice += 1
    points = points_sharing['price'] * (10 - slice_indice) / 10
    return round(points, 2)

def points_grade(grade, grade_min, grade_max):
    '''grade : float between 0 and 1'''
    if grade is None:
        return 0
    if grade_min == grade_max:
        return points_sharing['grade']
    relative_grade = (grade - grade_min) / (grade_max - grade_min)
    points = points_sharing['grade'] * relative_grade
    return round(points, 2)

def points_distance(distance, distance_min, distance_max):
    if distance_min == distance_max:
        return points_sharing['distance']
    relative_distance = (distance - distance_min) / (distance_max - distance_min)
    points = points_sharing['distance'] * (1 - relative_distance)
    return round(points, 2)

def points_wifi(wifi):
    return wifi * points_sharing['wifi']

def points_minibar(minibar):
    return minibar * points_sharing['minibar']

def points_clim(clim):
    return clim * points_sharing['clim']

def ranking_score(price, price_min, price_max, grade, grade_min, grade_max, distance, distance_min, distance_max, wifi, minibar, clim):
    pts_price = points_price(price, price_min, price_max)
    pts_grade = points_grade(grade, grade_min, grade_max)
    pts_distance = points_distance(distance, distance_min, distance_max)
    pts_services = points_wifi(wifi) + points_minibar(minibar) + points_clim(clim)
    return round(pts_price + pts_grade + pts_distance + pts_services, 2)

### Verify dates

class FormatError(Exception):
    pass

def verify_date_format(date):
    wanted_format = r"[0-9]{4}-[0-1][0-9]-[0-3][0-9]"
    if not re.match(wanted_format, date):
        raise FormatError

class PastDateError(Exception):
    pass

def verify_not_past_date(date_verified):
    [year, month, day] = date_verified.split('-')
    today = date.today()
    today_year = today.strftime("%Y")
    today_month = today.strftime("%m")
    today_day = today.strftime("%d")
    if year < today_year or (year == today_year and month < today_month) or (year == today_year and month == today_month and day < today_day):
        raise PastDateError

class DateOrder(Exception):
    pass

def verify_date_order(arrival_date, departure_date):
    [arr_year, arr_month, arr_day] = arrival_date.split('-')
    [dep_year, dep_month, dep_day] = departure_date.split('-')
    if dep_year < arr_year or (dep_year == arr_year and dep_month < arr_month) or (dep_year == arr_year and dep_month == arr_month and dep_day < arr_day):
        raise DateOrder
