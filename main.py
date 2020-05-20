import tkinter as tk
from tkinter import ttk, messagebox

from tripadvisor import *


def find_best_hotel(town, arrival_date, departure_date):
    conn = connection(town, arrival_date, departure_date)
    create_tables(conn)
    browser = setup_browser("/home/muller/Documents/Formation_JCS/scraping") #Path chromedriver for Alexandre
    #browser = setup_browser("./chromedriver")
    request(browser, town, arrival_date, departure_date)
    visit_hotels_all_pages(conn, browser)
    browser.close()
    fill_distances(conn, town)
    fill_points_table(conn)
    return ranking_all_hotels(conn)


class GraphicalInterface(tk.Frame):

    def __init__(self):
        self.window = tk.Tk()
        self.town = tk.StringVar(value="Fougères")
        self.arrival_date = tk.StringVar(value="2020-06-23")
        self.departure_date = tk.StringVar(value="2020-06-24")
        self.result_list = []
        self.hotel_labels = []

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

    def display_results(self):
        ttk.Label(self.window, text="Classement des hôtels disponibles", font='-weight bold').grid(row=5, columnspan=3)
        nb_hotels = len(self.result_list)
        for i in range(nb_hotels):
            if i == 0:
                text_color = 'red'
            else:
                text_color = 'black'
            hotel_name = self.result_list[i][0]
            score = self.result_list[i][1]
            ttk.Label(self.window, text=str(i+1), foreground=text_color).grid(row=6+i, column=0)
            hotel_label = ttk.Label(self.window, text=hotel_name, foreground=text_color)
            self.hotel_labels.append(hotel_label)
            hotel_label.grid(row=6+i, column=1)
            hotel_label.bind("<Button-1>", lambda event, hotel_rank=i: self.display_hotel_info(hotel_rank))
            hotel_label.bind("<Enter>", lambda event, hotel_rank=i: self.color_enter(hotel_rank))
            hotel_label.bind("<Leave>", lambda event, hotel_rank=i: self.color_leave(hotel_rank))
            ttk.Label(self.window, text="Score : " + str(score), foreground=text_color).grid(row=6+i, column=2)
        ttk.Label(self.window, text="Cliquez sur un hôtel pour obtenir plus d'informations.", font="-slant italic -size 10").grid(row=6+nb_hotels, columnspan=3)
        window_height = 150 + 22 * (nb_hotels + 1)
        self.window.geometry('550x{}'.format(str(window_height)))


    def color_enter(self, hotel_rank):
        label = self.hotel_labels[hotel_rank]
        label.config(font="-weight bold")

    def color_leave(self, hotel_rank):
        label = self.hotel_labels[hotel_rank]
        label.config(font='TkDefaultFont')

    def display_hotel_info(self, hotel_rank):
        '''hotel rank starts to 0, position of the hotel in the result_list'''
        hotel_name, score, address, price, grade, distance, wifi, minibar, clim = self.result_list[hotel_rank]
        info_window = tk.Toplevel(self.window)
        info_window.title("Détails sur un hôtel")
        ttk.Label(info_window, text="Nom de l'hôtel : {}".format(hotel_name)).pack(anchor='w')
        ttk.Label(info_window, text="Score obtenu : {}".format(score)).pack(anchor='w')
        ttk.Label(info_window, text="Adresse : {}".format(address)).pack(anchor='w')
        ttk.Label(info_window, text="Prix : {} euros".format(price)).pack(anchor='w')
        ttk.Label(info_window, text="Moyenne des avis : {} / 10".format(round(grade * 10, 1))).pack(anchor='w')
        ttk.Label(info_window, text="Distance au centre ville (ou à l'office de tourisme) : {} km".format(distance)).pack(anchor='w')
        ttk.Label(info_window, text="Présence de wifi : {}".format('oui' if wifi else 'non')).pack(anchor='w')
        ttk.Label(info_window, text="Présence d'un minibar : {}".format('oui' if minibar else 'non')).pack(anchor='w')
        ttk.Label(info_window, text="Présence de climatisation : {}".format('oui' if clim else 'non')).pack(anchor='w')

interface = GraphicalInterface()
interface.init_window()
interface.window.mainloop()
