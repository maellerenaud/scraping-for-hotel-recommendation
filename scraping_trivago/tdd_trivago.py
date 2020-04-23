#Bibliothèque selenium
from selenium import webdriver
import time
import os

### TTD

def ttd_connexion_home_page():
    return (connexion_home_page()) #Test class of the form

### Code
def connexion_home_page():
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("--start-maximised") #"kiosk" sur mac
    browser = webdriver.Chrome(executable_path="/home/muller/Documents/Formation_JCS/scraping/chromedriver", options=option)
    browser.get('https://www.trivago.fr/')

    try:
        search_form = browser.find_element_by_xpath('//form[@class="js-dealform dealform dealform--no-detail"]')
        return ("La connexion est réussie")

print (ttd_connexion_home_page())