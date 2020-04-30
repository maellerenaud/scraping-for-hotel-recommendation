import unittest

from utils import *

class TestUtils(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
