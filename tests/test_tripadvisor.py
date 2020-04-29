import unittest

from tripadvisor import *

class TestFunctions(unittest.TestCase):

    def test_adapt_dates_to_tripadvisor(self):
        self.assertEqual(adapt_dates_to_tripadvisor('2020-5-17'), '2020-4-17')
        self.assertEqual(adapt_dates_to_tripadvisor('2022-1-29'), '2022-0-29')

    def test_month_difference(self):
        self.assertEqual(month_difference('2020-4-27', '2020-5-27'), 1)
        self.assertEqual(month_difference('2020-4-27', '2020-4-27'), 0)
        self.assertEqual(month_difference('2020-11-27', '2021-1-4'), 2)


class TestSelenium(unittest.TestCase):

    def test_request(self):
        browser = setup_browser(r"/chromedriver")
        request(browser, 'Rennes', '2020-5-27', '2020-5-29')
        self.assertEqual(browser.current_url, "https://www.tripadvisor.fr/Hotels-g187103-Rennes_Ille_et_Vilaine_Brittany-Hotels.html")
        browser = setup_browser(r"/chromedriver")
        request(browser, 'Nantes', '2020-5-29', '2020-6-2')
        self.assertEqual(browser.current_url, "https://www.tripadvisor.fr/Hotels-g187198-Nantes_Loire_Atlantique_Pays_de_la_Loire-Hotels.html")

    def test_visit_hotels_one_page(self):
        browser = setup_browser(r"/chromedriver")
        request(browser, 'Rennes', '2020-5-27', '2020-5-28')
        self.assertEqual(visit_hotels_one_page(browser), 11)

    def test_visit_hotels_all_pages(self):
        browser = setup_browser(r"/chromedriver")
        request(browser, 'Rennes', '2020-5-27', '2020-5-28')
        self.assertEqual(visit_hotels_all_pages(browser), 11)
        browser = setup_browser(r"/chromedriver")
        request(browser, 'Toulouse', '2020-5-25', '2020-5-26')
        self.assertEqual(visit_hotels_all_pages(browser), 61)


class TestGetCharacteristics(unittest.TestCase):

    def test_get_name(self):
        browser = setup_browser(r"/chromedriver")
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d1186655-Reviews-Hotel_The_Originals_Rennes_Sud_La_Chaussairie-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_name(browser), "Hotel The Originals Rennes Sud La Chaussairie")

    def test_get_price(self):
        browser = setup_browser(r"/chromedriver")
        request(browser, 'Rennes', '2020-5-27', '2020-5-28')
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d2064905-Reviews-Novotel_SPA_Rennes_Centre_Gare-Rennes_Ille_et_Vilaine_Brittany.html')
        time.sleep(1)
        self.assertEqual(get_price(browser), 176)
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d235656-Reviews-Garden_Hotel-Rennes_Ille_et_Vilaine_Brittany.html')
        time.sleep(1)
        self.assertEqual(get_price(browser), 191)

    def test_get_grade(self):
        browser = setup_browser(r"/chromedriver")
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d2064905-Reviews-Novotel_SPA_Rennes_Centre_Gare-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_grade(browser), (4717/5745, 1149))

    def test_get_address(self):
        browser = setup_browser(r"/chromedriver")
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d2064905-Reviews-Novotel_SPA_Rennes_Centre_Gare-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_address(browser), "22 Avenue Jean Janvier, 35000, Rennes France")
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d1186655-Reviews-Hotel_The_Originals_Rennes_Sud_La_Chaussairie-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_address(browser), "30 Avenue De La Chaussairie Chartres De Bretagne, 35131, Rennes France")

    def test_get_services_on_services_page(self):
        browser = setup_browser(r"/chromedriver")
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d2064905-Reviews-Novotel_SPA_Rennes_Centre_Gare-Rennes_Ille_et_Vilaine_Brittany.html')
        time.sleep(2)
        plus = browser.find_element_by_xpath('//div[@id="ABOUT_TAB"]/div[1]/div[2]/div[1]/div[3]')
        plus.click()
        time.sleep(1)
        self.assertEqual(get_services_on_services_page(browser), (True, False, False))

    def test_get_services_on_hotel_page(self):
        browser = setup_browser(r"/chromedriver")
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d2064905-Reviews-Novotel_SPA_Rennes_Centre_Gare-Rennes_Ille_et_Vilaine_Brittany.html')
        time.sleep(2)
        self.assertEqual(get_services_on_hotel_page(browser, True), (False, True, True))


    def test_get_services(self):
        browser = setup_browser(r"/chromedriver")
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d2064905-Reviews-Novotel_SPA_Rennes_Centre_Gare-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_services(browser), (True, True, True))
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d1545570-Reviews-Sejours_Affaires_Bretagne_Rennes-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_services(browser), (True, False, False))
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d12099897-Reviews-Hisseo-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_services(browser), (False, False, False))
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d308006-Reviews-Auberge_de_Jeunesse_de_Rennes-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_services(browser), (False, False, False))
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187147-d231051-Reviews-Hotel_Harvey-Paris_Ile_de_France.html')
        self.assertEqual(get_services(browser), (True, True, True))

    def test_get_all_characteristics(self):
        browser = setup_browser(r"/chromedriver")
        request(browser, 'Rennes', '2020-5-27', '2020-5-28')
        browser.get('https://www.tripadvisor.fr/Hotel_Review-g187103-d2064905-Reviews-Novotel_SPA_Rennes_Centre_Gare-Rennes_Ille_et_Vilaine_Brittany.html')
        self.assertEqual(get_all_characteristics(browser), ("Novotel SPA Rennes Centre Gare", 176, 4717/5745, 1149, "22 Avenue Jean Janvier, 35000, Rennes France", True, True, True))


if __name__ == '__main__':
    unittest.main()
