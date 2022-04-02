"""
@author: Weronika Hebda
"""

from read_yuma import read_yuma
import numpy as np
import math as m
from date2tow import date2tow
from satpos import satpos
from array import *

alm = 'almanac.yuma.week0150.589824.txt'
navall = read_yuma(alm)
a = 6378137
e2 = 0.00669438002290
def geo_to_xyz(fi, lam, h):
    N = a / np.sqrt(1 - e2 * np.sin(fi) ** 2)
    x = (N + h) * np.cos(fi) * np.cos(lam)
    y = (N + h) * np.cos(fi) * np.sin(lam)
    z = (N * (1 - e2) + h) * np.sin(fi)
    return x, y, z

def cw2(week,tow,hour,maska):
    A = np.zeros((0, 4))
    ilosc_sat = 0
    elewacje = [maska]*31

    #petla przechodzaca przez wszystkie satelity
    for ijj in range(0,31):
        nav = navall[ijj, :]
        # print("Dane dla epoki: ", ijj)
        xs, ys, zs = satpos(nav,week,tow)
        # print("\twspolrzedne satelity: ",xs,ys,zs)

        fi = np.deg2rad(52)
        lam = np.deg2rad(21)
        h = 100


        # xr wspolrzedne odbiornika (miejsce obserwacji)

        # xr,yr,zr wspolrzedne odbiornika (miejsce obserwacji)
        xr, yr, zr = geo_to_xyz(fi, lam, h)
        # print("\twspolrzedne odbiornika: ",xr,yr,zr)

        XyzR = np.array([xr, yr, zr])
        XyzS = np.array([xs, ys, zs])

        XyzSR = XyzS - XyzR
        [xsr, ysr, zsr] = XyzSR


        # macierz obrotu
        def Rneu(fi, lam):
            Rneu = np.array([[-np.sin(fi) * np.cos(lam), -np.sin(lam), np.cos(fi) * np.cos(lam)],
                             [-np.sin(fi) * np.sin(lam), np.cos(lam), np.cos(fi) * np.sin(lam)],
                             [np.cos(fi), 0, np.sin(fi)]]
                            )
            return Rneu

        Rneu = Rneu(fi, lam)

        Rneu2 = Rneu.T

        Xsrneu = np.dot(Rneu2, XyzSR)

        [n, e, u] = Xsrneu

        #elewacja i azymut jednego satelity w jednej godzinie
        Az = np.arctan2(e, n)
        Az = m.degrees(Az)
        el = np.arcsin(u / m.sqrt(n ** 2 + e ** 2 + u ** 2))
        el = m.degrees(el)
        r = np.linalg.norm(XyzSR)
        # r = np.sqrt(xsr**2+ysr**2+zsr**2)
        # print(r)

         ##zmienic

        if el > maska:
            A1 = np.array([[-(xs - xr) / r, -(ys - yr) / r, -(zs - zr) / r, 1]])
            ilosc_sat = ilosc_sat + 1
            A = np.append(A, A1, axis=0)
            ###nie wiesz ktora to godzina uzyc find!!!
            elewacje[ijj] = el


            # if ijj == 0:
            #     el_sat0.append(el)
            # if ijj == 1:
            #     el_sat1.append(el)
            # if ijj == 2:
            #     el_sat2.append(el)
            # if ijj == 3:
            #     el_sat3.append(el)
            # if ijj == 4:
            #     el_sat4.append(el)
            # if ijj == 5:
            #     el_sat5.append(el)
            # if ijj == 6:
            #     el_sat6.append(el)
            # if ijj == 7:
            #     el_sat7.append(el)
            # if ijj == 5:
            #     el_sat5.append(el)
    Q = np.linalg.inv(A.T @ A)
    GDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2] + Q[3, 3])
    PDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
    TDOP = np.sqrt(Q[3, 3])

    Qneu = Rneu.T @ Q[0:3, 0:3] @ Rneu

    HDOP = np.sqrt(Qneu[0, 0] + Qneu[1, 1])
    VDOP = np.sqrt(Qneu[2, 2])
    PDOP_neu = np.sqrt(Qneu[0, 0] + Qneu[1, 1] + Qneu[2, 2])

    return ilosc_sat,elewacje


