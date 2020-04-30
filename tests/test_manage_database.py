import unittest
import os
import sys

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
        save(conn, 'Hotel name 1', 'tripadvisor', 30, 0.85, 547, '1 rue Bahon Rault, Rennes', 2.5, True, False, True)
        save(conn, 'Hotel name 2', 'trivago', 59.99, None, None, '1 rue Bahon Rault, Rennes', None, True, False, True)
        fill_distances(conn, 'Rennes')
        cursor = conn.execute("""SELECT * FROM Results""")
        rows = cursor.fetchall()
        self.assertEqual(rows[0], (1, 'hotel name 1', 'tripadvisor', 30, 0.85, 547, '1 rue bahon rault rennes', 2.5, 1, 0, 1))
        self.assertEqual(rows[1], (2, 'hotel name 2', 'trivago', 59.99, None, None, '1 rue bahon rault rennes', 2.5, 1, 0, 1))
        conn.close()
        os.remove('./rennes-2020-5-27-2020-5-28.db')

if __name__ == '__main__':
    unittest.main()
