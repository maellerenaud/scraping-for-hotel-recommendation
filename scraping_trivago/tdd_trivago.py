#Bibliothèque selenium
from selenium import webdriver
import time
import os
import unittest
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#Get to the site
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--start-maximised")
browser = webdriver.Chrome(executable_path="/home/muller/Documents/Formation_JCS/scraping/chromedriver", options=option)
browser.get('https://www.trivago.fr/')

### TTD

class TestFunction(unittest.TestCase):
    """
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
    
    
    def test_get_information_hotel(self): #the test hotal has to be first in apparition order
        browser.get('https://www.trivago.fr/?aDateRange%5Barr%5D=2021-01-01&aDateRange%5Bdep%5D=2021-01-15&aPriceRange%5Bfrom%5D=0&aPriceRange%5Bto%5D=0&iRoomType=9&aRooms%5B0%5D%5Badults%5D=2&aRooms%5B0%5D%5Bchildren%5D%5B0%5D=10&aRooms%5B0%5D%5Bchildren%5D%5B1%5D=10&cpt2=21766%2F200&hasList=1&hasMap=0&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=20000&address=&addressGeoCode=&offset=0&ra=&overlayMode=checkIn')
        time.sleep(5)
        list_hotels_prov1= browser.find_elements_by_tag_name("li")
        hotel= list_hotels_prov1[5]
                
        information = get_information_hotel(hotel)
        self.assertEqual(information,['Le Saint Antoine Hotel & Spa, BW Premier Collection','27 avenue Jean Janvier',524,'1.0',0.9,True,False,True]) 
        #Nom,adresse,prix,distance,note,wifi,minibar,clim
    """
    def test_get_hotels(self):
        hotels=get_hotels('Rennes','2021-01-01','2021-01-15')
        self.assertGreater(len(hotels),100)

### Code

def scroll():
    SCROLL_PAUSE_TIME = 1.5
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def connexion_home_page():
    search_title= browser.find_element_by_xpath('//span[@class="hero__subtitle"]').text
    return (search_title)
    

def get_research(town,start_date,end_date):
    

    #Searching inputs of the form
    
    place_input = browser.find_element_by_xpath('//input[@id="querytext"]')
    place_input.click()
    place_input.send_keys(town)
    place_input.send_keys(Keys.ENTER)

    try :
        start_date_button = browser.find_element_by_xpath('//button[@class="dealform-button js-dealform-button-calendar dealform-button--checkin"]')
        start_date_button.click()
    except:
        pass
    time.sleep(2)
    click_date(start_date)
    
    try :
        end_date_button= browser.find_element_by_xpath('//button[@class="dealform-button js-dealform-button-calendar dealform-button--checkout"]')
        end_date_button.click()
    except:
        pass
    click_date(end_date)

    try: #version with no chambres
        try :
            family_button = browser.find_element_by_xpath('//button[@class=dealform-button dealform-button--guests js-dealform-button-guests"]')
            family_button.click()
        except:
            pass
        
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
        time.sleep(1)
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

def get_hotels(town,start_date,end_date):
    get_research(town,start_date,end_date)
    hotels_information=[]
    for j in range (5):
        time.sleep(2)
        list_hotels_prov= browser.find_elements(By.XPATH, '//li[@class="hotel-item item-order__list-item js_co_item"]')
        time.sleep(10)
        for i in list_hotels_prov:
            hotels_information.append(get_information_hotel(i))
        scroll()
        if j<4:
            button_next_page =  browser.find_element_by_xpath('//button[@class="btn btn--pagination btn--small btn--page-arrow btn--next"]')
            button_next_page.click()
    return (hotels_information)

def get_information_hotel(hotel):
    time.sleep(2)
    title= hotel.find_element_by_xpath('//span[@class="item-link name__copytext"]').get_attribute("title")
    information_distance = hotel.find_element_by_xpath('//p[@class="details-paragraph details-paragraph--location location-details"]').text
    distance = information_distance.split(' ')[2]
    price = int((hotel.find_element_by_xpath('//strong[@data-qa="recommended-price"]').text)[0:-1])
    note = None #default value
    try :
        note = float(hotel.find_element_by_xpath('//span[@class="review"]/span/span').text)/10
    except:
        pass
    time.sleep(2)
    get_adress_button = hotel.find_element_by_xpath('//span[@class="icon-ic slideout-toggle-ic icon-contain"]')
    get_adress_button.click()
    print("Bouton cliqué")
    time.sleep (5)
    adress = None #Default value
    try:
        adress= hotel.find_element_by_xpath('//span[@itemprop="streetAddress"]').text
    except:
        pass
    wifi= False
    mini_bar= False
    clim = False
    try :
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="link"]')))
        time.sleep(2) 
        liste_services = hotel.find_elements_by_xpath('//li[@class="unordered-list__item"]')
        for i in liste_services :
            if i.get_attribute("class")=='unordered-list__item':
                if ('Wi-fi' in i.text) or ('Internet' in i.text):
                    wifi= True
                elif i.text == "Climatisation":
                    clim= True
                elif i.text == 'Réfrégirateur':
                    mini_bar== True
    except:
        pass
    information = [title,adress,price,distance,note,wifi,mini_bar,clim] 
    #Nom,adresse,prix,distance,note,wifi,minibar,clim
    browser.execute_script("window.scrollTo(0,300)")
    return (information)
### Test

if __name__ == '__main__':
    unittest.main()
