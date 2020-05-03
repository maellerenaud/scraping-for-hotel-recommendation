import unittest
import os

from manage_database import *

class TestDatabase(unittest.TestCase):

    def test_connection(self):
        connection('Rennes', '2020-5-27', '2020-5-28')
        self.assertEqual(os.path.exists('./rennes-2020-5-27-2020-5-28.db'), True)
        os.remove('./rennes-2020-5-27-2020-5-28.db')
        self.assertEqual(os.path.exists('./rennes-2020-5-27-2020-5-28.db'), False)
        connection('New York', '2020-5-27', '2020-5-28')
        self.assertEqual(os.path.exists('./new-york-2020-5-27-2020-5-28.db'), True)
        os.remove('./new-york-2020-5-27-2020-5-28.db')
        self.assertEqual(os.path.exists('./new-york-2020-5-27-2020-5-28.db'), False)

    def test_create_tables(self):
        conn = connection('Rennes', '2020-5-27', '2020-5-28')
        create_tables(conn)
        tables_names = []
        cursor = conn.execute("""SELECT * FROM sqlite_master WHERE type='table';""")
        for row in cursor:
            tables_names.append(row[1])
        self.assertIn('Results', tables_names)
        self.assertIn('Points', tables_names)
        conn.close()
        os.remove('./rennes-2020-5-27-2020-5-28.db')

    def test_save(self):
        conn = connection('Rennes', '2020-5-27', '2020-5-28')
        create_tables(conn)
        save(conn, 'Hotel name 1', 'tripadvisor', 30, 0.85, 547, '1 rue Bahon Rault, Rennes', 2.5, True, False, True)
        save(conn, 'Hotel name 2', 'trivago', 59.99, None, None, '1 rue Bahon Rault, Rennes', None, True, False, True)
        cursor = conn.execute("""SELECT * FROM Results""")
        rows = cursor.fetchall()
        self.assertEqual(rows[0], (1, 'hotel name 1', 'tripadvisor', 30, 0.85, 547, '1 rue bahon rault rennes', 2.5, 1, 0, 1))
        self.assertEqual(rows[1], (2, 'hotel name 2', 'trivago', 59.99, None, None, '1 rue bahon rault rennes', None, 1, 0, 1))
        conn.close()
        os.remove('./rennes-2020-5-27-2020-5-28.db')

    def test_fill_distances(self):
        conn = connection('Rennes', '2020-5-27', '2020-5-28')
        create_tables(conn)
        save(conn, 'Garden Hôtel Rennes', 'tripadvisor', 30, 0.85, 547, '3 Rue Jean Marie Duhamel, 35000 Rennes', None, True, False, True)
        save(conn, 'Hotel name 2', 'trivago', 59.99, None, None, '1 rue Bahon Rault, Rennes', 1, True, False, True)
        fill_distances(conn, 'Rennes')
        cursor = conn.execute("""SELECT * FROM Results""")
        rows = cursor.fetchall()
        self.assertEqual(rows[0], (1, 'garden hôtel rennes', 'tripadvisor', 30, 0.85, 547, '3 rue jean marie duhamel 35000 rennes', 2.9, 1, 0, 1))
        self.assertEqual(rows[1], (2, 'hotel name 2', 'trivago', 59.99, None, None, '1 rue bahon rault rennes', 1, 1, 0, 1))
        conn.close()
        os.remove('./rennes-2020-5-27-2020-5-28.db')

    def test_fill_points_table(self):
        conn = connection('Rennes', '2020-5-27', '2020-5-28')
        create_tables(conn)
        save(conn, 'Hotel name 1', 'tripadvisor', 30, 0.85, 547, '1 rue Bahon Rault, Rennes', 2.5, True, False, True)
        save(conn, 'Hotel name 1', 'trivago', 59.99, None, None, '1 rue Bahon Rault, Rennes', None, False, False, False)
        save(conn, 'Hotel name 1', 'booking', 30, 0.6, 53, '1 rue Bahon Rault, Rennes', 2, True, False, False)
        save(conn, 'Hotel name 2', 'trivago', 59.99, 0.7, 1234, '1 rue Bahon Rault, Rennes', 1.2, False, False, True)
        save(conn, 'Hotel name 3', 'trivago', 80, 0.5, 1234, '1 rue Bahon Rault, Rennes', 3, False, False, False)
        fill_points_table(conn)
        cursor = conn.execute("""SELECT * FROM Points""")
        rows = cursor.fetchall()
        self.assertEqual(rows[0], ('hotel name 1', 30, 20, 11.11, 15, 0, 10, 86.11))
        self.assertEqual(rows[1], ('hotel name 2', 15, 17.78, 20, 0, 0, 10, 62.78))
        self.assertEqual(rows[2], ('hotel name 3', 3, 0, 0, 0, 0, 0, 3))
        conn.close()
        os.remove('./rennes-2020-5-27-2020-5-28.db')

    def test_hotel_with_best_score(self):
        conn = connection('Rennes', '2020-5-27', '2020-5-28')
        create_tables(conn)
        save(conn, 'Hotel name 1', 'tripadvisor', 30, 0.85, 547, '1 rue Bahon Rault, Rennes', None, True, False, True)
        save(conn, 'Hotel name 1', 'trivago', 59.99, None, None, '1 rue Bahon Rault, Rennes', None, False, False, False)
        save(conn, 'Hotel name 1', 'booking', 30, 0.6, 53, '1 rue Bahon Rault, Rennes', 3, True, False, False)
        save(conn, 'Hotel name 2', 'trivago', 59.99, 0.7, 1234, '1 rue Bahon Rault, Rennes', 1.2, False, False, True)
        save(conn, 'Hotel name 3', 'trivago', 80, 0.5, 1234, '1 rue Bahon Rault, Rennes', 3, False, False, False)
        fill_distances(conn, 'Rennes')
        fill_points_table(conn)
        self.assertEqual(hotel_with_best_score(conn), 'hotel name 1')
        conn.close()
        os.remove('./rennes-2020-5-27-2020-5-28.db')

if __name__ == '__main__':
    unittest.main()
