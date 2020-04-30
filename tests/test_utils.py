import unittest

from utils import *

class TestUtilsForDatbase(unittest.TestCase):

    def test_normalize_string(self):
        self.assertEqual(normalize_string('Hotel The Originals Rennes Sud La Chaussairie'), 'hotel the originals rennes sud la chaussairie')
        self.assertEqual(normalize_string('Mandarin Oriental, Paris'), 'mandarin oriental paris')
        self.assertEqual(normalize_string('La Réserve Paris - Hotel and Spa'), 'la réserve paris hotel and spa')
        self.assertEqual(normalize_string('Hôtel Kleber Champs-Élysées Tour Eiffel Paris'), 'hôtel kleber champs-élysées tour eiffel paris')
        self.assertEqual(normalize_string('19 rue Saulnier, 75009 Paris France'), '19 rue saulnier 75009 paris france')

    def test_convert_distance_string_into_float(self):
        self.assertEqual(convert_distance_string_into_float('3,2 km'), 3.2)
        self.assertEqual(convert_distance_string_into_float('200 m'), 0.2)
        self.assertEqual(convert_distance_string_into_float('56 km'), 56)

    def test_distance(self):
        address = normalize_string("22 Avenue Jean Janvier, 35000, Rennes France")
        self.assertEqual(get_distance("Rennes", address), 3.2)
        address = normalize_string('36 rue du Grenier Saint Lazare, 75003 Paris France')
        self.assertEqual(get_distance('Paris', address), 2.6)
        address = normalize_string('40 Rue de Saint-Quentin, 75010 Paris')
        self.assertEqual(get_distance('Paris', address), 0.6)
        address = normalize_string('Brit Hotel du Parc - Fougères, 5 Zone de La Pilais 35133 Lécousse FR, Lécousse')
        self.assertEqual(get_distance('Romagné', address), 3.1)


class TestUtilsForPoints(unittest.TestCase):

    def test_points_price(self):
        self.assertEqual(points_price(35, 0, 100), 21)
        self.assertEqual(points_price(75.99, 0, 100), 9)
        self.assertEqual(points_price(0, 0, 100), 30)
        self.assertEqual(points_price(100, 0, 100), 3)

    def test_points_grade(self):
        self.assertEqual(points_grade(0.8756, 0, 1), 17.51)
        self.assertEqual(points_grade(0.8, 0.7, 0.9), 10)

    def test_points_distance(self):
        self.assertEqual(points_distance(46, 0, 100), 10.8)
        self.assertEqual(points_distance(30, 20, 40), 10)
        self.assertEqual(points_distance(20, 20, 40), 20)
        self.assertEqual(points_distance(40, 20, 40), 0)

    def test_points_wifi(self):
        self.assertEqual(points_wifi(True), 15)
        self.assertEqual(points_wifi(False), 0)

    def test_points_minibar(self):
        self.assertEqual(points_minibar(True), 5)
        self.assertEqual(points_minibar(False), 0)

    def test_points_clim(self):
        self.assertEqual(points_clim(True), 10)
        self.assertEqual(points_clim(False), 0)

    def test_ranking_function(self):
        self.assertEqual(ranking_function(80, 50, 100, 8, 7, 9, 2, 0, 4, True, False, False), 50)

if __name__ == '__main__':
    unittest.main()
