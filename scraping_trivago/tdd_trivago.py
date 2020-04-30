#Bibliothèque selenium
from selenium import webdriver
import time
import os
import unittest
from datetime import date
from selenium.webdriver.common.keys import Keys

#Get to the site
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--start-maximised")
browser = webdriver.Chrome(executable_path="/home/muller/Documents/Formation_JCS/scraping/chromedriver", options=option)
browser.get('https://www.trivago.fr/')

### TTD

class TestFunction(unittest.TestCase):
    def test_connexion_home_page(self):
        self.assertEqual(connexion_home_page(),"Essayez de rechercher une ville, un hôtel ou même un lieu connu.")
    
    def test_click_date(self):
        start_date_button = browser.find_element_by_xpath('//button[@class="dealform-button js-dealform-button-calendar dealform-button--checkin"]')
        start_date_button.click()
        go_to_date='2021-01-01' # format date AAAA-MM-JJ
        calendar_date=click_date('2021-01-01')
        self.assertEqual(calendar_date,go_to_date)

    def test_get_research(self):
        hotel_test=get_research('Rennes','2021-01-01','2021-01-15') #array f hotelspossible
        self.assertEqual(hotel_test,'js_itemlist')

### Code

def connexion_home_page():
    search_title= browser.find_element_by_xpath('//span[@class="hero__subtitle"]').text
    return (search_title)
    

def get_research(town,start_date,end_date):
    

    #Searching inputs of the form
    
    place_input = browser.find_element_by_xpath('//input[@id="querytext"]')
    place_input.click()
    place_input.send_keys(town)
    place_input.send_keys(Keys.ENTER)

    start_date_button = browser.find_element_by_xpath('//button[@class="dealform-button js-dealform-button-calendar dealform-button--checkin"]')
    start_date_button.click()
    click_date(start_date)
    
    try :
        end_date_button= browser.find_element_by_xpath('//button[@class="dealform-button js-dealform-button-calendar dealform-button--checkout"]')
    except :
        end_date_button= browser.find_element_by_xpath('//button[@class="dealform-button js-dealform-button-calendar dealform-button--checkout dealform-button--highlight"]')
    end_date_button.click()
    click_date(end_date)

    try: #version with no chambres
        '''
        family_button = browser.find_element_by_xpath('//button[@class=dealform-button dealform-button--guests js-dealform-button-guests"]')
        family_button.click()
        '''
        children_input = browser.find_element_by_xpath('//div[@class="guest-selector__content clearfix"]/div[2]/div[1]/button[2]')
        children_input.click()
        children_input = browser.find_element_by_xpath('//div[@class="guest-selector__content clearfix"]/div[2]/div[1]/button[2]')
        children_input.click()
    
        for i in range (1,3):
            children_button = browser.find_element_by_xpath('//ul[@class="ages-input__list"]/li['+str(i)+']/select/option[12]')
            children_button.click()
    
        validation_button= browser.find_element_by_xpath('//button[@class="btn btn--primary btn--small btn--apply-config"]')
        validation_button.click()

    except: #version with chambres
        type_room_button = browser.find_element_by_xpath('//ul[@class="df_container_roomtype_selector df_dropdown"]/li[3]/button')
        type_room_button.click()
        children_button = browser.find_element_by_xpath('//div[@class="column childs clearfix"]/div/select/option[3]')
        children_button.click()
        for i in range (1,3):
            children_button = browser.find_element_by_xpath('//div[@class="room_children_container multi"]/div['+str(i)+']/div/select/option[12]')
            children_button.click()
    
        time.sleep(2)
        valid_children_button= browser.find_element_by_xpath('//button[@class="btn btn--small btn--tertiary fl-trailing confirm"]')
        valid_children_button.click()
    

    valid_form_button= browser.find_element_by_xpath('//button[@class="btn btn--primary btn--regular search-button js-search-button"]')
    valid_form_button.click()

    hotel_test= browser.find_element_by_xpath('//ol[@class="hotel-list item-order itemlist hotellist clearfix"]').get_attribute("id")
    return (hotel_test)

def click_date (go_to_date):
    dic_month={'Janvier':1,'Février':2,'Mars':3,'Avril':4,'Mai':5,'Juin':6,'Juillet':7,'Août':8,'Septembre':9,'Octobre':10,'Novembre':11,'Décembre':12}
    
    button_change_month = browser.find_element_by_xpath('//button[@class="cal-btn-next"]')

    #Get to the correct page
    go_to_year=int(go_to_date[0:4])
    go_to_month=int(go_to_date[5:7])
    
    current_date= browser.find_element_by_xpath('//th[@class="cal-heading-month"]').text
    current_month= dic_month[str(current_date).split(' ')[0]]
    current_year= int(str(current_date).split(' ')[1])
    
    while current_year!=go_to_year and current_month!=go_to_month:
        # Move calendar next_month
        button_change_month.click()
        #Recalculate date
        current_date= browser.find_element_by_xpath('//th[@class="cal-heading-month"]').text
        current_month= dic_month[str(current_date).split(' ')[0]]
        current_year= int(str(current_date).split(' ')[1])
    
    date= browser.find_element_by_xpath('//time[@datetime="'+go_to_date+'"]')
    date.click()
    date_check= browser.find_element_by_xpath('//time[@class="dealform-button__label"]').get_attribute("datetime")
    return (date_check)


### Test

if __name__ == '__main__':
    unittest.main()