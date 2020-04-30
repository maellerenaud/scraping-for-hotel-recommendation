from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def setup_browser(path_chromedriver):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximised") #"kiosk" sur mac
    prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
    option.add_experimental_option('prefs', prefs)
    #browser = webdriver.Chrome(executable_path=str(os.getcwd())+"\chromedriver", options=option) #!!! Executable à télécharger et path à changer
    browser = webdriver.Chrome(executable_path=path_chromedriver, options=option)
    return browser

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

def get_distance(town, address):
    browser = setup_browser(r"./chromedriver")
    town_url = "{}+office+de+toursime".format(town,)
    address_url = '+'.join(address.split(' '))
    url = "https://www.google.fr/maps/dir/{}/{}/".format(address_url, town_url)
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    button_car = wait.until(ec.presence_of_element_located((By.XPATH, '//button/div[@aria-label="Voiture"]')))
    button_car.click()
    wait = WebDriverWait(browser, 10)
    distance = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@id="section-directions-trip-0"]/div[2]/div[1]/div[1]/div[2]/div[1]'))).text
    return convert_distance_string_into_float(distance)
