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

from matplotlib.pyplot import rc, rcParams, grid
import matplotlib.patches as mpatches


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
def plot_skyplot(sat_positions):
    # sat_positions - [PRN, el, az] w stopniach
    rc('grid', color='gray', linewidth=1, linestyle='--')
    fontsize = 20
    rc('xtick', labelsize=fontsize)
    rc('ytick', labelsize=fontsize)
    rc('font', size=fontsize)
    # define colors

    color = '#B3DBCB'

    # start ploting
    fig = plt.figure(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.1,
                        top=0.85,
                        left=0.1,
                        right=0.74)
    ax = fig.add_subplot(polar=True)  # define a polar type of coordinates
    ax.set_theta_zero_location('N')  # ustawienie kierunku północy na górze wykresu
    ax.set_theta_direction(-1)  # ustawienie kierunku przyrostu azymutu w prawo

    PG = 0  # zliczanie satelitów GPS

    for (PRN, el, az) in sat_positions:
        PG += 1
        ### show sat number

        ax.annotate(PRN,
                    xy=(np.radians(az), 90 - el),
                    bbox=dict(boxstyle="round", fc=color, alpha=0.5),
                    horizontalalignment='center',
                    verticalalignment='bottom',
                    color='k',
                    size=15)
        #                     #

    gps = mpatches.Patch(color=color, label='{:02.0f}  GPS'.format(PG))
    plt.legend(handles=[gps], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # axis ticks descriptions
    ax.set_yticks(range(0, 90 + 10, 10))  # Define the yticks
    yLabel = ['90°', '', '', '60°', '', '', '30°', '', '', '']
    ax.set_yticklabels(yLabel)
    # saving and showing plot
    # plt.savefig('satellite_skyplot.pdf')
    plt.show()  # wyświetleni


def liczba_sat():
    dzien = int(Entry1.get())
    miesiac = int(Entry2.get())
    rok = int(Entry3.get())
    godzina = int(Entry_h.get())
    minuta = int(Entry_m.get())
    sekunda = int(Entry_s.get())
    fi = int(Entry4.get())
    lam = int(Entry5.get())
    maska = int(Entry6.get())

    example1 = datetime(rok, miesiac, dzien, godzina, minuta, sekunda)
    example2 = datetime(rok, miesiac, dzien, godzina, minuta, sekunda)

    date1 = [example1.year, example1.month, example1.day, example1.hour, example1.minute, example1.second]
    date2 = [example2.year, example2.month, example2.day, example2.hour, example2.minute, example2.second]
    date3 = [example2.year, example2.month, example2.day, example2.hour, example2.minute, example2.second]

    ilosc_sat_24h = []
    el_sat_tab = []
    DOP = []
    for i in range(0, 24):
        # data[3] = i
        week, tow = date2tow(date1)
        ilosc_sat, el_sat, dop, nvm = cw2(week, tow, i, maska, fi, lam)
        ilosc_sat_24h.append(ilosc_sat)
        DOP.append(dop)
        example1 += timedelta(hours=1)
        date1 = [example1.year, example1.month, example1.day, example1.hour, example1.minute, example1.second]

    for k in range(0, 144):
        week, tow = date2tow(date2)
        ilosc_sat, el_sat, nvm1, nvm2 = cw2(week, tow, k, maska, fi, lam)
        el_sat_tab.append(el_sat)
        example2 += timedelta(minutes=10)
        date2 = [example2.year, example2.month, example2.day, example2.hour, example2.minute, example2.second]

    # wykres liczby satelitów
    x1 = list(np.arange(0, 24))
    plt.plot(x1, ilosc_sat_24h, marker='o')
    plt.show()

    #wykres elewacji satelitów
    x2 = list(np.arange(0, 144))
    nr = 1
    for j in range(0, 31):
        el_sat0 = []
        for i in range(0, 144):
            el_sat0.append(el_sat_tab[i][j])
        plt.plot(x2, el_sat0, label='Satelita nr ' + str(nr))
        nr = nr + 1
    plt.title("Wykres elewacji satelitów")
    plt.xlabel("czas[min]")
    plt.ylabel("elewacja")
    # plt.legend()
    plt.show()

    #wykres DOP
    for j in range(0, 5):
        dopy = []
        for i in range(0, 24):
            dopy.append(DOP[i][j])
        plt.plot(x1, dopy)
    plt.show()

    #wykres skyplot
    week, tow = date2tow(date3)
    nvm3, nvm4, nvm5, sat_position = cw2(week, tow, i, maska, fi, lam)
    plot_skyplot(sat_position)


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
Label8 = Label(window, text="φ:", font=("TimesNewRoman",14), fg='black', bd=10, padx=5, pady=5)
Label9 = Label(window, text="λ:", font=("TimesNewRoman",14), fg='black', bd=10, padx=5, pady=5)
Label10 = Label(window, text="Maska: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label_h = Label(window, text="Godzina: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label_m = Label(window, text="Minuta: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)
Label_s = Label(window, text="Sekunda: ", font=("TimesNewRoman",14),
               fg='black', bd=10, padx=5, pady=5)


Label1.place(x=10, y=10)
Label2.place(x=10, y=50)
Label11.place(x=800, y=50)
Label3.place(x=10, y=100)
Label4.place(x=10, y=140)
Label5.place(x=110, y=140)
Label6.place(x=210, y=140)
Label7.place(x=10, y=220)
Label8.place(x=10, y=267)
Label9.place(x=230, y=267)
Label10.place(x=10, y=320)
Label_h.place(x=310, y=140)
Label_m.place(x=410, y=140)
Label_s.place(x=510, y=140)

Entry1 = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry2 = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry3 = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry4 = Entry(window, font = ("TimesNewRoman",15), width = 14)
Entry5 = Entry(window, font = ("TimesNewRoman",15), width = 14)
Entry6 = Entry(window, font = ("TimesNewRoman",15), width = 14)
Entry_h = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry_m = Entry(window, font = ("TimesNewRoman",15), width = 5)
Entry_s = Entry(window, font = ("TimesNewRoman",15), width = 5)

Entry1.insert(0, "25")
Entry2.insert(0, "2")
Entry3.insert(0, "2022")
Entry4.insert(0, "52")
Entry5.insert(0, "21")
Entry6.insert(0, "10")
Entry_h.insert(0, "0")
Entry_m.insert(0, "0")
Entry_s.insert(0, "0")

Entry1.place(x=25, y=190)
Entry2.place(x=125, y=190)
Entry3.place(x=225, y=190)
Entry_h.place(x=325, y=190)
Entry_m.place(x=425, y=190)
Entry_s.place(x=525, y=190)
Entry4.place(x=60, y=280)
Entry5.place(x=280, y=280)
Entry6.place(x=22.5, y=370)


Button1 = tk.Button(window, text="Rysuj", font = ("TimesNewRoman",13), command=liczba_sat)
Button1.place(x=50, y=450)

# wykres wysokosci(elewacji) satelitow od czasu
# print(el_sat_tab)
# print(el_sat_tab[0][0])

# print(el_sat0)


tk.mainloop()