import unittest

from main import *

class TestMain(unittest.TestCase):

    def test_main(self):
        ranking_hotels = find_best_hotel('Rennes', '2020-5-27', '2020-5-28')
        for row in ranking_hotels:
            print("Nom de l'hôtel : {}, Score : {}".format(row[0], row[1]))


class TestGraphicalInterface(unittest.TestCase):

    def test_init_window(self):
        interface = GraphicalInterface()
        interface.init_window()
        interface.window.mainloop()

    def test_display_window(self):
        interface = GraphicalInterface()
        interface.result_list = [('super hotel '+str(i), 75.25, 'adresse', 115, 0.725, 3.2, True, False, False) for i in range(10)]
        interface.init_window()
        interface.display_results()
        interface.window.mainloop()

    def test_search_command_without_error(self):
        interface = GraphicalInterface()
        interface.init_window()
        interface.search_command()
        interface.window.mainloop()

    def test_search_command_format_error(self):
        interface = GraphicalInterface()
        interface.arrival_date = tk.StringVar(value="2020/06/25")
        interface.init_window()
        interface.search_command()
        interface.window.mainloop()

    def test_search_command_past_date_error(self):
        interface = GraphicalInterface()
        interface.departure_date = tk.StringVar(value="2020-04-25")
        interface.init_window()
        interface.search_command()
        interface.window.mainloop()

    def test_search_command_past_date_error(self):
        interface = GraphicalInterface()
        interface.arrival_date = tk.StringVar(value="2020-06-06")
        interface.departure_date = tk.StringVar(value="2020-06-05")
        interface.init_window()
        interface.search_command()
        interface.window.mainloop()

    def test_display_hotel_info(self):
        interface = GraphicalInterface()
        interface.result_list = [('hotel name 1', 75, '1 rue bahon rault rennes', 30, 0.725, 3, True, False, True)]
        interface.init_window()
        interface.display_hotel_info(0)
        interface.window.mainloop()


if __name__ == '__main__':
    unittest.main()
