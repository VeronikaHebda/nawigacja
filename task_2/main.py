import numpy as np

from readrnx_studenci import *
from satpos import satpos
from hirvonen import hirvonen
import math as m

def fRneu(fi, lam):
    Rneu = np.array([[-np.sin(fi) * np.cos(lam), -np.sin(lam), np.cos(fi) * np.cos(lam)],
                     [-np.sin(fi) * np.sin(lam), np.cos(lam), np.cos(fi) * np.sin(lam)],
                     [np.cos(fi), 0, np.sin(fi)]]
                    )
    return Rneu

def obrot(xs,ys,zs,a):
    #a = np.deg2rad(a)
    first = np.array([[np.cos(a), np.sin(a), 0],
                      [-np.sin(a), np.cos(a), 0],
                      [0,0,1]])
    second = np.array([xs,ys,zs])
    xs_root = first@second
    return xs_root

# scieżka do pliku nawigacyjnego
nav_file = 'WROC00POL_R_20220800000_01D_GN.rnx'
# cieżka do pliku obserwacyjnego
obs_file = 'WROC00POL_R_20220800000_01D_30S_MO.rnx'

# zdefiniowanie czasu obserwacji: daty początkowej i końcowej
# dla pierwszej epoki z pliku będzie to:
time_start = [2022, 3, 21, 0, 0, 0]
time_end = [2022, 3, 21, 0, 0, 0]

# odczytanie danych z pliku obserwacyjnego
obs, iobs = readrnxobs(obs_file, time_start, time_end, 'G')
# odczytanie danych z pliku nawigacyjnego:
nav, inav = readrnxnav(nav_file)
# filtrowanie danych: satelity "unhealthy"

sat = 1
ind = inav==sat
nav1 = nav[ind,:]
inav1 = inav[ind]

"""
zdefiniowanie współrzędnych przybliżonych odbiornika - mogą to być współrzędne z nagłówka 
pliku obserwacyjnego, skopiowane "z palca" lub pobierane automatycznie z treci nagłówka
"""
xr = 3835751.6257
yr = 1177249.7445
zr = 4941605.0540

"""
Wprowadzenie ustawień, takich jak maska obserwacji, czy typ poprawki troposferycznej
"""
maska = 10  # elevation mask/cut off in degrees

"""
Przeliczenie daty początkowej i końcowej do sekund tygodnia GPS - niezbędne w celu
poprawnej definicji pętli związanej z czasem obserwacji w ciągu całej doby
"""
week, tow = date2tow(time_start)[0:2]
week_end, tow_end = date2tow(time_end)[0:2]

#Obliczenia
omegaE = 7.2921151467 * (10 ** (-5))
dt = 30
for t in range(tow, tow_end+1, dt):
    index = iobs[:, 2] == t
    sats = iobs[index, 0]
    p_obs = obs[index, 0]


dtr = 0
tau = 0.072
c = 299792458.0
tau_list = [0.072] * 32

for i in range(5):
    print("Iteracja numer:", i)
    A1 = np.zeros((0, 4))
    y1 = []
    for j,sat in enumerate(sats):
        print("Satelita numer:",sat)
        ind_sat = inav == sat
        nav_sat = nav[ind_sat]
        tr = 86400 - tau_list[j] + dtr
        print("tau:",tau_list[j])
        xs, ys, zs, dts,dtrel = satpos(nav_sat, week, tr)
        print("ts,wspolrzedne, dts",tr, xs, ys, zs, dts)
        if i==0:
            a = omegaE * tau
            dtr = 0
        else:
            a = omegaE * tau_list[j]
        xs_root = obrot(xs,ys,zs,a)
        print("xs root",xs_root)

        fi,lam,h = hirvonen(xr,yr,zr)
        XyzR = np.array([xr, yr, zr])
        XyzS = np.array([xs_root[0], xs_root[1], xs_root[2]])
        XyzSR = XyzS - XyzR
        Rneu = fRneu(fi, lam)
        Rneu2 = Rneu.T
        Xsrneu = np.dot(Rneu2, XyzSR)
        [n, e, u] = Xsrneu

        Az = np.arctan2(e, n)
        Az = m.degrees(Az)
        el = np.arcsin(u / m.sqrt(n ** 2 + e ** 2 + u ** 2))
        el = m.degrees(el)
        r = np.linalg.norm(XyzSR)
        print("az:",Az)
        print("el",el)
        print("r",r)

        if i==0:
            tau_list[j] = r / c
        if el > maska:
            Pcalc = r - c * dts + c * dtr
            print("pcalc", Pcalc)
            y = Pcalc - p_obs[j]
            y1.append(y)
            A = np.array([[-(xs_root[0] - xr) / r, -(xs_root[1] - yr) / r, -(xs_root[2] - zr) / r, 1]])
            A1 = np.append(A1, A, axis=0)
    print("y", y1)
    print("A", A1)
    x = - np.linalg.inv(A1.T @ A1) @ A1.T @ y1
    print("x",x)
    xr = (xr + x[0])
    yr = (yr + x[1])
    zr = (zr + x[2])
    dtr = (dtr + x[3]/c)
    print(xr,yr,zr,dtr)


"""

            Po skończeniu 5. iteracji, zbieramy obliczone współrzędne xr - warto zebrać również
            liczby obserwowanych satelitów, obliczone wartoci współczynników DOP (przynajmniej PDOP)

"""