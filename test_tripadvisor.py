import unittest

from tripadvisor import adapt_dates_to_tripadvisor, setup_browser, request, month_difference

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
        browser = setup_browser(r"/home/peach/PycharmProjects/scraping/chromedriver")
        request(browser, 'Rennes', '2020-4-27', '2020-4-29')
        self.assertEqual(browser.current_url, "https://www.tripadvisor.fr/Hotels-g187103-Rennes_Ille_et_Vilaine_Brittany-Hotels.html")
        browser = setup_browser(r"/home/peach/PycharmProjects/scraping/chromedriver")
        request(browser, 'Nantes', '2020-5-29', '2020-6-2')
        self.assertEqual(browser.current_url, "https://www.tripadvisor.fr/Hotels-g187198-Nantes_Loire_Atlantique_Pays_de_la_Loire-Hotels.html")


if __name__ == '__main__':
    unittest.main()
