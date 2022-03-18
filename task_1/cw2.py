"""
@author: Weronika Hebda
"""

from read_yuma import read_yuma
import numpy as np
import math as m
from date2tow import date2tow
from satpos import satpos

alm = 'almanac.yuma.week0150.589824.txt'
navall = read_yuma(alm)

data = [2022, 2, 25, 0, 0, 0]
week, tow = date2tow(data)
A = np.zeros((0, 4))
for ijj in range(0, 31):

    nav = navall[ijj, :]
    print("Dane dla epoki: ", ijj)
    xs, ys, zs = satpos(nav,week,tow)
    print("\twspolrzedne satelity: ", xs, ys, zs)

    a = 6378137
    e2 = 0.00669438002290

    fi = np.deg2rad(52)
    lam = np.deg2rad(21)
    h = 100


    # xr wspolrzedne odbiornika (miejsce obserwacji)

    def geo_to_xyz(fi, lam, h):
        N = a / np.sqrt(1 - e2 * np.sin(fi) ** 2)
        x = (N + h) * np.cos(fi) * np.cos(lam)
        y = (N + h) * np.cos(fi) * np.sin(lam)
        z = (N * (1 - e2) + h) * np.sin(fi)
        return x, y, z


    # xr,yr,zr wspolrzedne odbiornika (miejsce obserwacji)
    xr, yr, zr = geo_to_xyz(fi, lam, h)
    print("\twspolrzedne odbiornika: ", xr, yr, zr)

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

    Az = np.arctan2(e, n)
    Az = m.degrees(Az)
    el = np.arcsin(u / m.sqrt(n ** 2 + e ** 2 + u ** 2))
    el = m.degrees(el)

    print("\tEl:", el, "\t Az:", Az)

    r = np.linalg.norm(XyzSR)
    # r = np.sqrt(xsr**2+ysr**2+zsr**2)
    print(r)
    if el > 10:
        A1 = np.array([[-(xs - xr) / r, -(ys - yr) / r, -(zs - zr) / r, 1]])
        # print(A1)
        A = np.append(A, A1, axis=0)
print("A:",A)

Q = np.linalg.inv(A.T @ A)
print("Q:",Q)
GDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2] + Q[3, 3])
PDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
TDOP = np.sqrt(Q[3, 3])

Qneu = Rneu.T @ Q[0:3, 0:3] @ Rneu
print("Qneu:",Qneu)



