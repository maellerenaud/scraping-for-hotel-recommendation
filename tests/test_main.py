import unittest

from main import *

class TestMain(unittest.TestCase):

    def test_main(self):
        ranking_hotels = find_best_hotel('Rennes', '2020-5-27', '2020-5-28')
        for row in ranking_hotels:
            print("Nom de l'hôtel : {}, Score : {}".format(row[0], row[1]))


if __name__ == '__main__':
    unittest.main()
