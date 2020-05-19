import tkinter as tk
from tkinter import ttk, messagebox

from manage_database import *
from tripadvisor import *


def find_best_hotel(town, arrival_date, departure_date):
    conn = connection(town, arrival_date, departure_date)
    create_tables(conn)
    browser = setup_browser(r"../chromedriver")
    request(browser, town, arrival_date, departure_date)
    visit_hotels_all_pages(conn, browser)
    fill_distances(conn, town)
    fill_points_table(conn)
    return ranking_all_hotels(conn)


class GraphicalInterface(tk.Frame):

    def __init__(self):
        self.window = tk.Tk()
        self.town = tk.StringVar(value="Fougères")
        self.arrival_date = tk.StringVar(value="2020-06-25")
        self.departure_date = tk.StringVar(value="2020-06-26")
        self.result_list = []

    def init_window(self):
        self.window.geometry('480x150')
        self.window.title('Trouver le meilleur hôtel')
        # Town
        ttk.Label(self.window, text="Ville").grid(row=0, column=0)
        ttk.Entry(self.window, textvariable=self.town).grid(row=0, column=1)
        # Date format
        ttk.Label(self.window, text="Merci de renseigner les dates au format AAAA-MM-JJ.", justify="left").grid(row=1, columnspan=3)
        # Arrival date
        ttk.Label(self.window,text="Date d'arrivée").grid(row=2, column=0)
        ttk.Entry(self.window, textvariable=self.arrival_date).grid(row=2, column=1)
        # Departure date
        ttk.Label(self.window,text="Date de départ").grid(row=3, column=0)
        ttk.Entry(self.window, textvariable=self.departure_date).grid(row=3, column=1)
        # Button
        ttk.Button(self.window, text="Chercher", command=self.search_command).grid(row=4, column=0)

    def display_results(self):
        ttk.Label(self.window, text="Classement des hôtels disponibles").grid(row=5, columnspan=3)
        nb_hotels = len(self.result_list)
        for i in range(nb_hotels):
            if i == 0:
                text_color = 'red'
            else:
                text_color = 'black'
            hotel_name, score = self.result_list[i]
            ttk.Label(self.window, text=str(i+1), foreground=text_color).grid(row=6+i, column=0)
            ttk.Label(self.window, text=hotel_name, foreground=text_color).grid(row=6+i, column=1)
            ttk.Label(self.window, text="Score : " + str(score), foreground=text_color).grid(row=6+i, column=2)
        window_height = 150 + 22 * nb_hotels
        self.window.geometry('550x{}'.format(str(window_height)))

    def search_command(self):
        try :
            verify_date_format(self.arrival_date.get())
            verify_date_format(self.departure_date.get())
            verify_not_past_date(self.arrival_date.get())
            verify_not_past_date(self.departure_date.get())
            verify_date_order(self.arrival_date.get(), self.departure_date.get())
            self.result_list = find_best_hotel(self.town.get(), self.arrival_date.get(), self.departure_date.get())
            self.display_results()
        except FormatError:
            messagebox.showerror("Erreur de date", "Le format attendu est AAAA-MM-JJ.")
        except PastDateError:
            messagebox.showerror("Erreur de date", "Les dates proposées sont passées.")
        except DateOrder:
            messagebox.showerror("Erreur de date", "La date de départ est antérieure à celle d'arrivée.")
