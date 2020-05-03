from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from datetime import date

from manage_database import *

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
    wait = WebDriverWait(browser, 10)
    button_date = wait.until(ec.visibility_of_element_located((By.XPATH, '//span[@data-date="{}"]'.format(adapted_date,))))
    button_date.click()

def chose_both_dates(browser, search_bar, arrival_date, departure_date):
    open_calendar = search_bar.find_element_by_xpath('//span[@data-datetype="CHECKIN"]')
    open_calendar.click()
    time.sleep(1)
    today = str(date.today())
    for i in range(month_difference(today, arrival_date)):
        wait = WebDriverWait(browser, 10)
        next_month = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="rsdc-next rsdc-nav ui_icon single-chevron-right-circle"]')))
        next_month.click()
        time.sleep(1)
    chose_date(browser, arrival_date)
    chose_date(browser, departure_date)     # No need to change month, we can reserve only for 30 days maximum

def chose_guests(browser, search_bar):
    open_guests_choice = search_bar.find_element_by_xpath('//div[@data-prwidget-name="ibex_trip_search_rooms_guests"]')
    open_guests_choice.click()
    wait = WebDriverWait(browser, 10)
    button_add_child = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="childrenPlaceholder"]/div[1]/span[1]/span[@class="ui_icon plus-circle"]')))
    button_add_child.click()
    button_add_child.click()
    children_ages_wrap = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="ages-wrap"]')))
    for i in range(1,3):
        open_child_age_choices = children_ages_wrap.find_element_by_xpath('./span[{}]/span[1]/span[2]'.format(str(i)))
        open_child_age_choices.click()
        children_ages_wrap.find_element_by_xpath('./span[{}]/span[1]/div[1]/span[1]/ul[2]/li[@data-val="10"]'.format(str(i))).click()
        time.sleep(1)

def request(browser, town, arrival_date, departure_date):
    browser.get('https://www.tripadvisor.fr/Hotels')
    wait = WebDriverWait(browser, 3)
    search_bar = wait.until(ec.presence_of_element_located((By.XPATH, '//div[@id="taplc_trip_search_home_hotels_0"]/div[2]')))
    chose_town(search_bar, town)
    chose_both_dates(browser, search_bar, arrival_date, departure_date)
    chose_guests(browser, search_bar)
    search_button = browser.find_element_by_xpath('//button[@id="SUBMIT_HOTELS"]')
    search_button.click()

### Get charateristics of one hotel

def get_name(browser):
    wait = WebDriverWait(browser, 3)
    name = wait.until(ec.presence_of_element_located((By.XPATH, '//h1[@id="HEADING"]')))
    return name.text

def get_price(browser):
    try:
        wait = WebDriverWait(browser, 3)
        offers = wait.until(ec.visibility_of_any_elements_located((By.XPATH, '//div[@class="hotels-hotel-offers-DetailChevronOffer__price--py2LH"]')))
        best_offer = offers[0]
    except:
        wait = WebDriverWait(browser, 10)
        best_offer = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="hotels-hotel-offers-DominantOffer__price--D-ycN"]')))
    price = int(best_offer.text[:-1])
    return price

def get_grade(browser):
    try:
        wait = WebDriverWait(browser, 10)
        votes = wait.until(ec.visibility_of_all_elements_located((By.XPATH, '//ul[@class="location-review-review-list-parts-ReviewFilter__filter_table--1H9KD"]/li/span[2]')))
        grade_votes = {}
        grade = 5
        for element in votes:
            grade_votes[grade] = int(element.text)
            grade -= 1
        nb_votes = grade_votes[1] + grade_votes[2] + grade_votes[3] + grade_votes[4] + grade_votes[5]
        average =  (grade_votes[1] + grade_votes[2]*2 + grade_votes[3]*3 + grade_votes[4]*4 + grade_votes[5]*5) / (nb_votes*5)
        return average, nb_votes
    except:
        return None

def get_address(browser):
    wait = WebDriverWait(browser, 10)
    address = wait.until(ec.presence_of_element_located((By.XPATH, '//div[@class="public-business-listing-ContactInfo__offer--KAFI4 public-business-listing-ContactInfo__location--1jP2j"]/span[2]')))
    return address.text

def get_services_on_services_page(browser):
    wifi, clim, minibar = False, False, False
    wait = WebDriverWait(browser, 3)
    services = wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[@class="hotels-hr-about-amenities-AmenitiesModal__group--3nudN"]/div')))
    for service in services:
        wifi = wifi or service.text == 'Wi-Fi'
        clim = clim or service.text == 'Climatisation'
        minibar = minibar or service.text == 'Minibar'
    wait = WebDriverWait(browser, 3)
    quit = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="_2EFRp_bb _3IWKziRc _3ptEwvMl"][@role="button"]')))
    quit.click()
    return wifi, clim, minibar

def get_services_on_hotel_page(browser, room_services):
    wifi, clim, minibar = False, False, False
    if room_services:
        wait = WebDriverWait(browser, 3)
        services = wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[@class="hotels-hr-about-amenities-AmenityGroup__amenitiesList--3MdFn"][2]/div')))
    else:
        wait = WebDriverWait(browser, 3)
        services = wait.until(ec.presence_of_all_elements_located((By.XPATH, '//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[@class="hotels-hr-about-amenities-AmenityGroup__amenitiesList--3MdFn"][1]/div')))
    for service in services:
        wifi = wifi or service.text == 'Wi-Fi'
        clim = clim or service.text == 'Climatisation'
        minibar = minibar or service.text == 'Minibar'
    return wifi, clim, minibar

def get_services(browser):
    wifi, clim, minibar = False, False, False
    # Get hotel services
    try:
        wait = WebDriverWait(browser, 3)
        plus = wait.until(ec.presence_of_element_located((By.XPATH, '//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[3]')))
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
        wait = WebDriverWait(browser, 3)
        plus = wait.until(ec.presence_of_element_located((By.XPATH, '//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[6]')))
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

def get_all_characteristics(conn, browser):
    name = get_name(browser)
    price = get_price(browser)
    grade, nb_votes = get_grade(browser)
    address = get_address(browser)
    wifi, clim, minibar = get_services(browser)
    save(conn, name, 'tripadvisor', price, grade, nb_votes, address, None, wifi, minibar, clim)

### Visit all hotels pages

def visit_hotels_one_page(conn, browser):
    time.sleep(5)
    wait = WebDriverWait(browser, 10)
    available_hotels = wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]')))
    time.sleep(3)
    list_hotels = available_hotels.find_elements_by_xpath('.//a[@data-clicksource="HotelName"]')
    nb_hotels = len(list_hotels) - 1
    print(nb_hotels)
    for i in range(nb_hotels):
        wait = WebDriverWait(browser, 10)
        list_hotels = wait.until(ec.visibility_of_all_elements_located((By.XPATH, '//a[@data-clicksource="HotelName"]')))
        hotel = list_hotels[i]
        browser.get(hotel.get_attribute('href'))
        get_all_characteristics(conn, browser)
        browser.back()
    return nb_hotels

def visit_hotels_all_pages(conn, browser):
    nb_hotels_visited = visit_hotels_one_page(conn, browser)
    wait = WebDriverWait(browser, 10)
    list_hotels = wait.until(ec.visibility_of_all_elements_located((By.XPATH, '//a[@data-clicksource="HotelName"]')))
    nb_hotels_on_page = len(list_hotels)
    total_nb_hotels_visited = nb_hotels_visited
    i = 2
    while nb_hotels_visited == nb_hotels_on_page:
        try:
            next_page = browser.find_element_by_xpath('//div[@class="pageNumbers"]/a[{}]'.format(str(i),)).get_attribute('href')
            browser.get(next_page)
            nb_hotels_visited = visit_hotels_one_page(conn, browser)
            wait = WebDriverWait(browser, 10)
            nb_hotels_on_page = len(wait.until(ec.visibility_of_all_elements_located((By.XPATH, '//a[@data-clicksource="HotelName"]'))))
            total_nb_hotels_visited += nb_hotels_visited
            i += 1
        except:
            break
    return total_nb_hotels_visited

