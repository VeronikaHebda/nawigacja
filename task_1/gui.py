from read_yuma import read_yuma
import numpy as np
import math as m
from cw2 import cw2
from date2tow import date2tow
from datetime import datetime, timedelta

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog

window = Tk()
window.geometry("1920x1080")
window.title("Systemy nawigacji satelitarnej zad_1")


# fala = np.arange(400, 1601, 10)
# fig = Figure(figsize=(6, 4), dpi=100)  # matplotlib Figure
# ax = fig.add_subplot(xlabel = "x", ylabel = "y")
# ax.set_title("Należność punktów do wielokąta")
# ax.grid()
# canvas = FigureCanvasTkAgg(fig, master=window)  # master = jakastam_frame
# canvas.get_tk_widget().place(x=10,y=20)
# canvas.draw()  # w funkcji rysowania

# toolbar = NavigationToolbar2Tk(canvas,window)
# toolbar.place(x = 220, y = 430)


def liczba_sat():
    maska = int(Entry4.get())
    # data = [2022, 2, 25, 0, 0, 0]

    example = datetime(2022, 2, 25, 0, 0, 0)
    date1 = [example.year, example.month, example.day, example.hour, example.minute, example.second]

    ilosc_sat_24h = []
    for i in range(0, 24):
        # data[3] = i

        week, tow = date2tow(date1)
        ilosc_sat, el_sat = cw2(week, tow, i, maska)
        ilosc_sat_24h.append(ilosc_sat)
        example += timedelta(hours=1)
        date1 = [example.year, example.month, example.day, example.hour, example.minute, example.second]
    # wykres liczby satelitów
    x1 = list(np.arange(0, 24))
    plt.plot(x1, ilosc_sat_24h, marker='o')
    plt.show()


def wysokosc_sat():
    maska = int(Entry6.get())
    el_sat_tab = []
    example = datetime(2022, 2, 25, 0, 0, 0)
    date2 = [example.year, example.month, example.day, example.hour, example.minute, example.second]
    x2 = list(np.arange(0, 144))
    for k in range(0, 144):
        week, tow = date2tow(date2)
        ilosc_sat, el_sat = cw2(week, tow, k, maska)
        el_sat_tab.append(el_sat)
        example += timedelta(minutes=10)
        date2 = [example.year, example.month, example.day, example.hour, example.minute, example.second]

    for j in range(0, 31):
        el_sat0 = []
        for i in range(0, 144):
            el_sat0.append(el_sat_tab[i][j])
        plt.plot(x2, el_sat0)
    plt.show()


Label1 = Label(window, text="Aplikacja do planowania pomiarów GNSS ", font=("TimesNewRoman",17,'bold'),
               fg='black', bd=10, padx=5, pady=5)
Label2 = Label(window, text="Wprowadź dane: ", font=("TimesNewRoman",15,'bold'),
               fg='black', bd=10, padx=5, pady=5)
Label11 = Label(window, text="Wyniki: ", font=("TimesNewRoman",15,'bold'),
               fg='black', bd=10, padx=5, pady=5)
Label3 = Label(window, text="Data obserwacji: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label4 = Label(window, text="Dzień: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label5 = Label(window, text="Miesiąc: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label6 = Label(window, text="Rok: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label7 = Label(window, text="Miejsce obserwacji - wprowadź współrzędne geograficzne: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label8 = Label(window, text="φ", font=("TimesNewRoman",14), fg='black')
Label9 = Label(window, text="λ", font=("TimesNewRoman",14), fg='black')
Label10 = Label(window, text="Maska: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)


Label1.place(x=10, y=10)
Label2.place(x=10, y=50)
Label11.place(x=800, y=50)
Label3.place(x=10, y=100)
Label4.place(x=10, y=140)
Label5.place(x=140, y=140)
Label6.place(x=280, y=140)
Label7.place(x=10, y=220)
Label8.place(x=90, y=260)
Label9.place(x=310, y=260)
Label10.place(x=10, y=350)

Entry1 = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry2 = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry3 = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry4 = Entry(window, font = ("TimesNewRoman",15), width = 14)
Entry5 = Entry(window, font = ("TimesNewRoman",15), width = 14)
Entry6 = Entry(window, font = ("TimesNewRoman",15), width = 14)

Entry1.place(x=25, y=190)
Entry2.place(x=155, y=190)
Entry3.place(x=295, y=190)
Entry4.place(x=22.5, y=300)
Entry5.place(x=240, y=300)
Entry6.place(x=22.5, y=400)


Button1 = tk.Button(window, text="Rysuj", font = ("TimesNewRoman",13), command=wysokosc_sat)
Button1.place(x=10, y=450)

# wykres wysokosci(elewacji) satelitow od czasu
# print(el_sat_tab)
# print(el_sat_tab[0][0])

# print(el_sat0)


tk.mainloop()