from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from datetime import date
import os

### Set up browser

def setup_browser(path_chromedriver):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximised") #"kiosk" sur mac
    prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
    option.add_experimental_option('prefs', prefs)
    #browser = webdriver.Chrome(executable_path=str(os.getcwd())+"\chromedriver", options=option) #!!! Executable à télécharger et path à changer
    browser = webdriver.Chrome(executable_path=path_chromedriver, options=option)
    return browser

### Connect to tripadvisor and make request

def adapt_dates_to_tripadvisor(date):
    """ date in format "year-month-day" """
    list = date.split('-')
    list[1] = str(int(list[1]) - 1)
    return '-'.join(list)

def chose_town(search_bar, town):
    picker_town = search_bar.find_element_by_xpath('./div[1]/div[1]/span[1]/input[1]')
    picker_town.send_keys(town)

def month_difference(date1, date2):
    list1 = date1.split('-')
    list2 = date2.split('-')
    return int(list2[1]) - int(list1[1]) + 12 * (int(list2[0]) - int(list1[0]))

def chose_date(browser, date):
    adapted_date = adapt_dates_to_tripadvisor(date)
    button_date = browser.find_element_by_xpath('//span[@data-date="{}"]'.format(adapted_date,))
    button_date.click()

def chose_both_dates(browser, search_bar, arrival_date, departure_date):
    open_calendar = search_bar.find_element_by_xpath('//span[@data-datetype="CHECKIN"]')
    open_calendar.click()
    time.sleep(1)
    today = str(date.today())
    for i in range(month_difference(today, arrival_date)):
        browser.find_element_by_xpath('//div[@class="rsdc-next rsdc-nav ui_icon single-chevron-right-circle"]').click()
        time.sleep(1)
    chose_date(browser, arrival_date)
    chose_date(browser, departure_date)     # No need to change month, we can reserve only for 30 days maximum

def chose_guests(browser, search_bar):
    open_guests_choice = search_bar.find_element_by_xpath('//div[@data-prwidget-name="ibex_trip_search_rooms_guests"]')
    open_guests_choice.click()
    button_add_child = browser.find_element_by_xpath('//div[@class="childrenPlaceholder"]/div[1]/span[1]/span[@class="ui_icon plus-circle"]')
    button_add_child.click()
    time.sleep(0.5)
    button_add_child.click()
    time.sleep(0.5)
    children_ages_wrap = browser.find_element_by_xpath('//div[@class="ages-wrap"]')
    for i in range(1,3):
        open_child_age_choices = children_ages_wrap.find_element_by_xpath('./span[{}]/span[1]/span[2]'.format(str(i)))
        open_child_age_choices.click()
        children_ages_wrap.find_element_by_xpath('./span[{}]/span[1]/div[1]/span[1]/ul[2]/li[@data-val="10"]'.format(str(i))).click()
        time.sleep(0.5)

def request(browser, town, arrival_date, departure_date):
    browser.get('https://www.tripadvisor.fr/Hotels')
    time.sleep(1)
    search_bar = browser.find_element_by_xpath('//div[@id="taplc_trip_search_home_hotels_0"]/div[2]')
    chose_town(search_bar, town)
    chose_both_dates(browser, search_bar, arrival_date, departure_date)
    chose_guests(browser, search_bar)
    search_button = browser.find_element_by_xpath('//button[@id="SUBMIT_HOTELS"]')
    search_button.click()
    time.sleep(1)

### Get charateristics of one hotel and save them

def get_price(browser):
    best_offer = browser.find_element_by_xpath('//div[@class="hotels-hotel-offers-DominantOffer__price--D-ycN"]')
    price = int(best_offer.text[:-1])
    return price

def get_grade(browser):
    votes = browser.find_elements_by_xpath('//ul[@class="location-review-review-list-parts-ReviewFilter__filter_table--1H9KD"]/li/span[2]')
    grade_votes = {}
    grade = 5
    for element in votes:
        grade_votes[grade] = int(element.text)
        grade -= 1
    nb_votes = grade_votes[1] + grade_votes[2] + grade_votes[3] + grade_votes[4] + grade_votes[5]
    average =  (grade_votes[1] + grade_votes[2]*2 + grade_votes[3]*3 + grade_votes[4]*4 + grade_votes[5]*5) / (nb_votes*5)
    return average, nb_votes

def get_localisation(browser):
    indice = browser.find_element_by_xpath('//div[@id="LOCATION"]/div[2]/div[1]/span[1]').text
    return int(indice)

def get_services_on_services_page(browser):
    wifi, clim, minibar = False, False, False
    services = browser.find_elements_by_xpath('//div[@class="hotels-hr-about-amenities-AmenitiesModal__group--3nudN"]/div')
    for service in services:
        wifi = wifi or service.text == 'Wi-Fi'
        clim = clim or service.text == 'Climatisation'
        minibar = minibar or service.text == 'Minibar'
    quit = browser.find_element_by_xpath('//div[@class="_2EFRp_bb _3IWKziRc _3ptEwvMl"][@role="button"]')
    quit.click()
    return wifi, clim, minibar

def get_services_on_hotel_page(browser, room_services):
    wifi, clim, minibar = False, False, False
    if room_services:
        services = browser.find_elements_by_xpath('//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[@class="hotels-hr-about-amenities-AmenityGroup__amenitiesList--3MdFn"][2]/div')
    else:
        services = browser.find_elements_by_xpath('//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[@class="hotels-hr-about-amenities-AmenityGroup__amenitiesList--3MdFn"][1]/div')
    for service in services:
        wifi = wifi or service.text == 'Wi-Fi'
        clim = clim or service.text == 'Climatisation'
        minibar = minibar or service.text == 'Minibar'
    return wifi, clim, minibar

def get_services(browser):
    wifi, clim, minibar = False, False, False
    # Get hotel services
    try:
        plus = browser.find_element_by_xpath('//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[3]')
        plus.click()
        time.sleep(1)
        wifi1, clim1, minibar1 = get_services_on_services_page(browser)
        wifi, clim, minibar = wifi or wifi1, clim or clim1, minibar or minibar1
    except:
        try:
            wifi2, clim2, minibar2 = get_services_on_hotel_page(browser, False)
            wifi, clim, minibar = wifi or wifi2, clim or clim2, minibar or minibar2
        except:
            pass
    # Get room services
    try:
        plus = browser.find_element_by_xpath('//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[6]')
        plus.click()
        time.sleep(1)
        wifi3, clim3, minibar3 = get_services_on_services_page(browser)
        wifi, clim, minibar = wifi or wifi3, clim or clim3, minibar or minibar3
    except:
        try:
           wifi4, clim4, minibar4 = get_services_on_hotel_page(browser, True)
           wifi, clim, minibar = wifi or wifi4, clim or clim4, minibar or minibar4
        except:
            pass
    return wifi, clim, minibar


