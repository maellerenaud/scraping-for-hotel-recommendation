from selenium import webdriver
import time
from datetime import date
import os

#Introduction necessaire au module selenium
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--start-maximised") #"kiosk" sur mac
prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
option.add_experimental_option('prefs', prefs)
#browser = webdriver.Chrome(executable_path=str(os.getcwd())+"\chromedriver", options=option) #!!! Executable à télécharger et path à changer
browser = webdriver.Chrome(executable_path=r"/home/peach/PycharmProjects/scraping/chromedriver", options=option)


def adapt_dates_to_tripadvisor(date):
    """ date in format "year-month-day" """
    list = date.split('-')
    list[1] = str(int(list[1]) - 1)
    return '-'.join(list)


def setup_browser(path_chromedriver):
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximised") #"kiosk" sur mac
    prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
    option.add_experimental_option('prefs', prefs)
    #browser = webdriver.Chrome(executable_path=str(os.getcwd())+"\chromedriver", options=option) #!!! Executable à télécharger et path à changer
    browser = webdriver.Chrome(executable_path=path_chromedriver, options=option)
    return browser

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


