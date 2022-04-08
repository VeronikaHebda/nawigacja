

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:28:09 2022

@author: Student1
"""

import numpy as np
from oblicz import cw2
from date2tow import date2tow
from datetime import datetime, timedelta

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style

import matplotlib.patches as mpatches
from math import degrees, atan2, pi, asin

windows = Tk()
windows.geometry("1920x1080")
windows.title("Systemy nawigacji satelitarnej zad_1")

style = Style()
style.theme_create("MyStyle", parent="alt", settings={
    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
    "TNotebook.Tab": {"configure": {"padding": [30, 15]}, }})
style.theme_use("MyStyle")
notebook = ttk.Notebook(windows)
tab1 = Frame(notebook)
tab2 = Frame(notebook)
notebook.add(tab1, text="Zakładka 1")
notebook.add(tab2, text="Zakładka 2")
notebook.pack(expand=True, fill="both")
# notebook.place(x = 1000, y = 80)

fig1 = Figure(figsize=(6, 4), dpi=100)  # matplotlib Figure
ax1 = fig1.add_subplot(xlabel="czas [h]", ylabel="liczba satelitów")
ax1.set_title("Wykres liczby satelitów")
ax1.grid()
canvas1 = FigureCanvasTkAgg(fig1, master=tab1)  # master = jakastam_frame
canvas1.get_tk_widget().place(x=680, y=120)
canvas1.draw()  # w funkcji rysowania

fig2 = plt.figure(figsize=(6, 4), dpi=100)  # matplotlib Figure
plt.subplots_adjust(bottom=0.1,
                    top=0.85,
                    left=0.1,
                    right=0.74)
ax2 = fig2.add_subplot(xlabel="czas [h]", ylabel="elewacja")
ax2.set_title("Wykres elewacji satelitów")
ax2.grid()
canvas2 = FigureCanvasTkAgg(fig2, master=tab1)  # master = jakastam_frame
canvas2.get_tk_widget().place(x=1300, y=120)
# w funkcji rysowania

fig3 = Figure(figsize=(6, 4), dpi=100)  # matplotlib Figure
ax3 = fig3.add_subplot(xlabel="czas [h]", ylabel="wartość współczynnika")
ax3.set_title("Wykres DOP")
ax3.grid()
canvas3 = FigureCanvasTkAgg(fig3, master=tab1)  # master = jakastam_frame
canvas3.get_tk_widget().place(x=680, y=550)
canvas3.draw()  # w funkcji rysowania

fig4 = plt.figure(figsize=(6, 4), dpi=100)
plt.subplots_adjust(bottom=0.1,
                    top=0.85,
                    left=0.1,
                    right=0.74)
ax4 = fig4.add_subplot(polar=True)  # define a polar type of coordinates
ax4.set_title("Wykres rozmieszczenia satelitów")
ax4.set_theta_zero_location('N')  # ustawienie kierunku północy na górze wykresu
ax4.set_theta_direction(-1)  # ustawienie kierunku przyrostu azymutu w prawo
canvas4 = FigureCanvasTkAgg(fig4, master=tab1)  # master = jakastam_frame
canvas4.get_tk_widget().place(x=1300, y=550)
canvas4.draw()  # w funkcji rysowania

w, h = plt.figaspect(0.5)
fig5 = plt.figure(figsize=(w, h), dpi=80)  # matplotlib Figure
ax5 = fig5.add_subplot(xlabel="Longitude $[\mathrm{^\circ}]$", ylabel="Latitude $[\mathrm{^\circ}]$")
plt.subplots_adjust(bottom=0.1,
                    top=0.85,
                    left=0.1,
                    right=0.74)
ax5.set_title("Wykres drogi satelitów")
ax5.grid()
canvas5 = FigureCanvasTkAgg(fig5, master=tab2)  # master = jakastam_frame
canvas5.get_tk_widget().place(x=50, y=120)
canvas5.draw()  # w funkcji rysowania

w, h = plt.figaspect(0.5)
fig6 = plt.figure(figsize=(w, h), dpi=80)  # matplotlib Figure
ax6 = fig6.add_subplot(xlabel="Longitude $[\mathrm{^\circ}]$", ylabel="Latitude $[\mathrm{^\circ}]$")
ax6.set_title("Wykres globalnej widoczności satelit")
ax6.grid()
canvas6 = FigureCanvasTkAgg(fig6, master=tab2)  # master = jakastam_frame
canvas6.get_tk_widget().place(x=50, y=550)
canvas6.draw()  # w funkcji rysowania


# fig5 = plt.figure(figsize=(w, h))
def groundtrack_latlon(R):
    # R = [xs, ys, zs]
    r_delta = np.linalg.norm(R[0:1])
    sinA = R[1] / r_delta
    cosA = R[0] / r_delta

    Lon = atan2(sinA, cosA)

    if Lon < - pi:
        Lon = Lon + 2 * pi
    Lat = asin(R[2] / np.linalg.norm(R))
    filam = []
    filam.append(degrees(Lon))
    filam.append(degrees(Lat))
    return filam


def rysuj():
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()

    ax1.set_xlabel("czas [h]")
    ax1.set_ylabel("liczba satelitów")
    ax1.set_title("Wykres liczby satelitów")
    ax1.grid()

    ax2.set_title("Wykres elewacji satelitów")
    ax2.set_xlabel("czas [h]")
    ax2.set_ylabel("elewacja")
    ax2.grid()

    ax3.set_xlabel("czas [h]")
    ax3.set_ylabel("wartość współczynnika")
    ax3.set_title("Wykres DOP")
    ax3.grid()

    ax4.set_title("Wykres rozmieszczenia satelitów")
    ax4.set_theta_zero_location('N')  # ustawienie kierunku północy na górze wykresu
    ax4.set_theta_direction(-1)  # ustawienie kierunku przyrostu azymutu w prawo

    dzien = int(Entry1.get())
    miesiac = int(Entry2.get())
    rok = int(Entry3.get())
    godzina = int(Entry_h.get())
    minuta = int(Entry_m.get())
    sekunda = int(Entry_s.get())
    fi = int(Entry4.get())
    lam = int(Entry5.get())
    maska = int(Entry6.get())
    nr_sat = int(Entry7.get())
    zaznaczone = []
    for i in range (0,31):
        zaznaczone.append(zmienne[i].get())

    example2 = datetime(rok, miesiac, dzien, godzina, minuta, sekunda)

    date2 = [example2.year, example2.month, example2.day, example2.hour, example2.minute, example2.second]
    date3 = [example2.year, example2.month, example2.day, example2.hour, example2.minute, example2.second]

    ilosc_sat_24h = []
    el_sat_tab = []
    xyz_tab = []
    DOP = []
    data_label=[]
    for k in range(0, 144):
        week, tow = date2tow(date2)
        ilosc_sat, el_sat, dop, nvm2, xyz, nvm7 = cw2(week, tow, maska, fi, lam, 50, zaznaczone)
        ilosc_sat_24h.append(ilosc_sat)
        DOP.append(dop)
        el_sat_tab.append(el_sat)
        xyz_tab.append(xyz)
        if k % 12 == 0:
            data_label.append(date2[3])
        example2 += timedelta(minutes=10)
        date2 = [example2.year, example2.month, example2.day, example2.hour, example2.minute, example2.second]

    # wykres liczby satelitów
    x1 = list(np.arange(0, 144))
    ticks = list(np.arange(0,144,12))
    ax1.plot(x1, ilosc_sat_24h)
    ax1.set_xticks(ticks)
    ax1.set_xticklabels(data_label)
    # ax1.set_axisbelow(True)
    canvas1.draw()

    # wykres elewacji satelitów
    nr = 1

    for j in range(0, 31):
        el_sat0 = []
        for i in range(0, 144):
            el_sat0.append(el_sat_tab[i][j])
        if zmienne[j].get() != 0:
            ax2.plot(x1, el_sat0, label='PG' + str(nr))
        nr = nr + 1

    # plt.legend(handles=[gps], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=15)
    ax2.legend(title='Numer satelitów', title_fontsize=9, ncol=2, loc='center left', bbox_to_anchor=(1, 0.57),
               fontsize=7)
    ax2.set_axisbelow(True)
    ax2.set_xticks(ticks)
    ax2.set_xticklabels(data_label)
    canvas2.draw()

    # wykres DOP
    count = 0
    for j in range(0, 5):
        dopy = []
        for i in range(0, 144):
            dopy.append(DOP[i][j])
        if count == 0:
            ax3.plot(x1, dopy, label="GDOP")
        elif count == 1:
            ax3.plot(x1, dopy, label="PDOP")
        elif count == 2:
            ax3.plot(x1, dopy, label="TDOP")
        elif count == 3:
            ax3.plot(x1, dopy, label="HDOP")
        elif count == 4:
            ax3.plot(x1, dopy, label="VDOP")
        count = + 1
    ax3.legend()
    ax3.set_axisbelow(True)
    ax3.set_xticks(ticks)
    ax3.set_xticklabels(data_label)
    canvas3.draw()

    # wykres skyplot
    week, tow = date2tow(date3)
    widocznosc = []

    nvm3, nvm4, nvm5, sat_positions, nv6, widocznosc = cw2(week, tow, maska, fi, lam, nr_sat, zaznaczone)
    # define colors

    kolor = '#B3DBCB'

    # start ploting

    PG = 0  # zliczanie satelitów GPS

    for (PRN, el, az) in sat_positions:
        PG += 1
        ### show sat number

        ax4.annotate(PRN,
                     xy=(np.radians(az), 90 - el),
                     bbox=dict(boxstyle="round", fc=kolor, alpha=0.5),
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     color='k',
                     size=10)
        #                     #

    gps = mpatches.Patch(color=kolor, label='{:02.0f}  GPS'.format(PG))
    ax4.legend(handles=[gps], bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=15)

    # axis ticks descriptions
    ax4.set_yticks(range(0, 90 + 10, 10))  # Define the yticks
    yLabel = ['90°', '', '', '60°', '', '', '30°', '', '', '']
    ax4.set_yticklabels(yLabel)
    # saving and showing plot
    # plt.savefig('satellite_skyplot.pdf')
    ax4.set_axisbelow(True)
    canvas4.draw()

    # groundtrack

    # GENERAL setup

    # params = {'legend.fontsize': 8, 'legend.handlelength': 2}
    # rcParams.update(params)
    fi_lamda_tab = []

    xyz_tab2 = []
    for j in range(0, 31):
        for i in range(0, 144):
            xyz_tab2.append(xyz_tab[i][j])

    for i in range(4464):
        fi_lamda_tab.append(groundtrack_latlon(xyz_tab2[i]))

    coastline_data = np.loadtxt('Coastline.txt', skiprows=1)

    # ax5 = fig5.gca()  # add iteratively

    fig5.suptitle('Wykres drogi satelitów', fontsize=16)
    ax5.set_xlabel('Longitude $[\mathrm{^\circ}]$', fontsize=14)
    ax5.set_ylabel('Latitude $[\mathrm{^\circ}]$', fontsize=14)
    ax5.plot(coastline_data[:, 0], coastline_data[:, 1], 'g', linewidth=0.5)
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    plt.yticks([-90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    plt.xticks([-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180])

    nr = 1

    for j in range(0, 31):
        el_sat1 = []
        lon_ground = []
        lat_ground = []
        if zmienne[j].get() != 0:
            for i in range(j * 144, (j + 1) * 144):
                el_sat1.append(fi_lamda_tab[i])
            for pos in el_sat1:
                lon_ground.append(pos[0])
                lat_ground.append(pos[1])
                # print(lon_ground, lat_ground)
            ax5.scatter(lon_ground, lat_ground, s=5, label='PG' + str(nr))
            nr = nr + 1

    ax5.legend(title='Numer satelitów', title_fontsize=15, ncol=2, loc='center left',
               bbox_to_anchor=(1, 0.57), fontsize=11)
    ax5.grid(True)
    canvas5.draw()

    # groundtracking
    ax6.plot(coastline_data[:, 0], coastline_data[:, 1], 'g', linewidth=0.5)
    ax6.imshow(widocznosc, alpha=0.7, extent=[-180, 180, -90, 90])
    fig6.suptitle('Wykres globalnej widoczności satelity nr'+str(nr_sat), fontsize=16)
    ax6.set_xlabel('Longitude $[\mathrm{^\circ}]$', fontsize=14)
    ax6.set_ylabel('Latitude $[\mathrm{^\circ}]$', fontsize=14)
    canvas6.draw()

Label1 = Label(windows, text="Aplikacja do planowania pomiarów GNSS ", font=("TimesNewRoman", 17, 'bold'),
               fg='black', bd=10, padx=5, pady=5)
Label2 = Label(tab1, text="Wprowadź dane: ", font=("TimesNewRoman", 15, 'bold'),
               fg='black', bd=10, padx=5, pady=5)
Label11 = Label(tab1, text="Wyniki: ", font=("TimesNewRoman", 15, 'bold'),
                fg='black', bd=10, padx=5, pady=5)
Label12 = Label(tab2, text="Wyniki c.d: ", font=("TimesNewRoman", 15, 'bold'),
                fg='black', bd=10, padx=5, pady=5)
Label3 = Label(tab1, text="Data obserwacji: ", font=("TimesNewRoman", 14),
               fg='black', bd=10, padx=5, pady=5)
Label4 = Label(tab1, text="Dzień: ", font=("TimesNewRoman", 14),
               fg='black', bd=10, padx=5, pady=5)
Label5 = Label(tab1, text="Miesiąc: ", font=("TimesNewRoman", 14),
               fg='black', bd=10, padx=5, pady=5)
Label6 = Label(tab1, text="Rok: ", font=("TimesNewRoman", 14),
               fg='black', bd=10, padx=5, pady=5)
Label7 = Label(tab1, text="Miejsce obserwacji - wprowadź współrzędne geograficzne: ", font=("TimesNewRoman", 14),
               fg='black', bd=10, padx=5, pady=5)
Label8 = Label(tab1, text="φ:", font=("TimesNewRoman", 14), fg='black', bd=10, padx=5, pady=5)
Label9 = Label(tab1, text="λ:", font=("TimesNewRoman", 14), fg='black', bd=10, padx=5, pady=5)
Label10 = Label(tab1, text="Maska: ", font=("TimesNewRoman", 14),
                fg='black', bd=10, padx=5, pady=5)
Label13 = Label(tab1, text="Wybór satelitów: ", font=("TimesNewRoman", 14),
                fg='black', bd=10, padx=5, pady=5)
Label14 = Label(tab1, text="Wpisz nr satelity do globalnej widoczności: ", font=("TimesNewRoman", 14),
                fg='black', bd=10, padx=5, pady=5)
Label_h = Label(tab1, text="Godzina: ", font=("TimesNewRoman", 14),
                fg='black', bd=10, padx=5, pady=5)
Label_m = Label(tab1, text="Minuta: ", font=("TimesNewRoman", 14),
                fg='black', bd=10, padx=5, pady=5)
Label_s = Label(tab1, text="Sekunda: ", font=("TimesNewRoman", 14),
                fg='black', bd=10, padx=5, pady=5)

Label1.place(x=10, y=55)
Label2.place(x=10, y=50)
Label11.place(x=800, y=50)
Label12.place(x=10, y=50)
Label3.place(x=10, y=100)
Label4.place(x=10, y=140)
Label5.place(x=110, y=140)
Label6.place(x=210, y=140)
Label7.place(x=10, y=220)
Label8.place(x=10, y=267)
Label9.place(x=230, y=267)
Label10.place(x=10, y=320)
Label13.place(x=10, y=420)
Label14.place(x=10, y=770)
Label_h.place(x=310, y=140)
Label_m.place(x=410, y=140)
Label_s.place(x=510, y=140)

Entry1 = Entry(tab1, font=("TimesNewRoman", 15), width=5)
Entry2 = Entry(tab1, font=("TimesNewRoman", 15), width=5)
Entry3 = Entry(tab1, font=("TimesNewRoman", 15), width=5)
Entry4 = Entry(tab1, font=("TimesNewRoman", 15), width=14)
Entry5 = Entry(tab1, font=("TimesNewRoman", 15), width=14)
Entry6 = Entry(tab1, font=("TimesNewRoman", 15), width=14)
Entry7 = Entry(tab1, font=("TimesNewRoman", 15), width=14)
Entry_h = Entry(tab1, font=("TimesNewRoman", 15), width=5)
Entry_m = Entry(tab1, font=("TimesNewRoman", 15), width=5)
Entry_s = Entry(tab1, font=("TimesNewRoman", 15), width=5)

Entry1.insert(0, "25")
Entry2.insert(0, "2")
Entry3.insert(0, "2022")
Entry4.insert(0, "52")
Entry5.insert(0, "21")
Entry6.insert(0, "10")
Entry7.insert(0, "3")
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
Entry7.place(x=22.5, y=820)


def zaznacz():
    satelita1.select()
    satelita2.select()
    satelita3.select()
    satelita4.select()
    satelita5.select()
    satelita6.select()
    satelita7.select()
    satelita8.select()
    satelita9.select()
    satelita10.select()
    satelita11.select()
    satelita12.select()
    satelita13.select()
    satelita14.select()
    satelita15.select()
    satelita16.select()
    satelita17.select()
    satelita18.select()
    satelita19.select()
    satelita20.select()
    satelita21.select()
    satelita22.select()
    satelita23.select()
    satelita24.select()
    satelita25.select()
    satelita26.select()
    satelita27.select()
    satelita28.select()
    satelita29.select()
    satelita30.select()
    satelita31.select()


def odznacz():
    satelita1.deselect()
    satelita2.deselect()
    satelita3.deselect()
    satelita4.deselect()
    satelita5.deselect()
    satelita6.deselect()
    satelita7.deselect()
    satelita8.deselect()
    satelita9.deselect()
    satelita10.deselect()
    satelita11.deselect()
    satelita12.deselect()
    satelita13.deselect()
    satelita14.deselect()
    satelita15.deselect()
    satelita16.deselect()
    satelita17.deselect()
    satelita18.deselect()
    satelita19.deselect()
    satelita20.deselect()
    satelita21.deselect()
    satelita22.deselect()
    satelita23.deselect()
    satelita24.deselect()
    satelita25.deselect()
    satelita26.deselect()
    satelita27.deselect()
    satelita28.deselect()
    satelita29.deselect()
    satelita30.deselect()
    satelita31.deselect()


Button1 = tk.Button(tab1, text="Rysuj", font=("TimesNewRoman", 13, "bold"), command=rysuj,
                    width=20, activebackground="gray")
Button1.place(x=170, y=870)
Button2 = tk.Button(tab1, text="Zaznacz wszystkie", font=("TimesNewRoman", 13), command=zaznacz,
                    width=20, activebackground="gray")
Button2.place(x=50, y=720)
Button3 = tk.Button(tab1, text="Odznacz wszystkie", font=("TimesNewRoman", 13), command=odznacz,
                    width=20, activebackground="gray")
Button3.place(x=300, y=720)

q = BooleanVar()
w = BooleanVar()
e = BooleanVar()
r = BooleanVar()
t = BooleanVar()
y = BooleanVar()
u = BooleanVar()
i = BooleanVar()
o = BooleanVar()
p = BooleanVar()
a = BooleanVar()
s = BooleanVar()
d = BooleanVar()
f = BooleanVar()
g = BooleanVar()
h = BooleanVar()
j = BooleanVar()
k = BooleanVar()
l = BooleanVar()
z = BooleanVar()
x = BooleanVar()
c = BooleanVar()
v = BooleanVar()
b = BooleanVar()
n = BooleanVar()
m = BooleanVar()
qw = BooleanVar()
we = BooleanVar()
er = BooleanVar()
rt = BooleanVar()
ty = BooleanVar()

zmienne = []
zmienne.append(q)
zmienne.append(w)
zmienne.append(e)
zmienne.append(r)
zmienne.append(t)
zmienne.append(y)
zmienne.append(u)
zmienne.append(i)
zmienne.append(o)
zmienne.append(p)
zmienne.append(a)
zmienne.append(s)
zmienne.append(d)
zmienne.append(f)
zmienne.append(g)
zmienne.append(h)
zmienne.append(j)
zmienne.append(k)
zmienne.append(l)
zmienne.append(z)
zmienne.append(x)
zmienne.append(c)
zmienne.append(v)
zmienne.append(b)
zmienne.append(n)
zmienne.append(m)
zmienne.append(qw)
zmienne.append(we)
zmienne.append(er)
zmienne.append(rt)
zmienne.append(ty)

satelita1 = Checkbutton(tab1, text="PG1", variable=q, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita2 = Checkbutton(tab1, text="PG2", variable=w, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita3 = Checkbutton(tab1, text="PG3", variable=e, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita4 = Checkbutton(tab1, text="PG4", variable=r, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita5 = Checkbutton(tab1, text="PG5", variable=t, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita6 = Checkbutton(tab1, text="PG6", variable=y, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita7 = Checkbutton(tab1, text="PG7", variable=u, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita8 = Checkbutton(tab1, text="PG8", variable=i, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita9 = Checkbutton(tab1, text="PG9", variable=o, onvalue=1, offvalue=0,
                        font=("TimesNewRoman", 15))
satelita10 = Checkbutton(tab1, text="PG10", variable=p, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita11 = Checkbutton(tab1, text="PG11", variable=a, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita12 = Checkbutton(tab1, text="PG12", variable=s, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita13 = Checkbutton(tab1, text="PG13", variable=d, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita14 = Checkbutton(tab1, text="PG14", variable=f, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita15 = Checkbutton(tab1, text="PG15", variable=g, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita16 = Checkbutton(tab1, text="PG16", variable=h, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita17 = Checkbutton(tab1, text="PG17", variable=j, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita18 = Checkbutton(tab1, text="PG18", variable=k, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita19 = Checkbutton(tab1, text="PG19", variable=l, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita20 = Checkbutton(tab1, text="PG20", variable=z, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita21 = Checkbutton(tab1, text="PG21", variable=x, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita22 = Checkbutton(tab1, text="PG22", variable=c, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita23 = Checkbutton(tab1, text="PG23", variable=v, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita24 = Checkbutton(tab1, text="PG24", variable=b, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita25 = Checkbutton(tab1, text="PG25", variable=n, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita26 = Checkbutton(tab1, text="PG26", variable=m, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita27 = Checkbutton(tab1, text="PG27", variable=qw, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita28 = Checkbutton(tab1, text="PG29", variable=we, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita29 = Checkbutton(tab1, text="PG30", variable=er, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita30 = Checkbutton(tab1, text="PG31", variable=rt, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
satelita31 = Checkbutton(tab1, text="PG32", variable=ty, onvalue=1, offvalue=0,
                         font=("TimesNewRoman", 15))
# satelita1.select()
satelita2.select()
# satelita3.select()
satelita4.select()
# satelita5.select()
# satelita6.select()
satelita7.select()
# satelita8.select()
# satelita9.select()
# satelita10.select()
# satelita11.select()
# satelita12.select()
# satelita13.select()
satelita14.select()
satelita15.select()
# satelita16.select()
satelita17.select()
# satelita18.select()
# satelita19.select()
# satelita20.select()
# satelita21.select()
# satelita22.select()
# satelita23.select()
satelita24.select()
# satelita25.select()
# satelita26.select()
# satelita27.select()
# satelita28.select()
# satelita29.select()
# satelita30.select()
# satelita31.select()

satelita1.place(x=20, y=470)
satelita2.place(x=20, y=500)
satelita3.place(x=20, y=530)
satelita4.place(x=20, y=560)
satelita5.place(x=20, y=590)
satelita6.place(x=20, y=620)
satelita7.place(x=20, y=650)
satelita8.place(x=20, y=680)
satelita9.place(x=180, y=470)
satelita10.place(x=180, y=500)
satelita11.place(x=180, y=530)
satelita12.place(x=180, y=560)
satelita13.place(x=180, y=590)
satelita14.place(x=180, y=620)
satelita15.place(x=180, y=650)
satelita16.place(x=180, y=680)
satelita17.place(x=360, y=470)
satelita18.place(x=360, y=500)
satelita19.place(x=360, y=530)
satelita20.place(x=360, y=560)
satelita21.place(x=360, y=590)
satelita22.place(x=360, y=620)
satelita23.place(x=360, y=650)
satelita24.place(x=360, y=680)
satelita25.place(x=540, y=470)
satelita26.place(x=540, y=500)
satelita27.place(x=540, y=530)
satelita28.place(x=540, y=560)
satelita29.place(x=540, y=590)
satelita30.place(x=540, y=620)
satelita31.place(x=540, y=650)

tk.mainloop()

