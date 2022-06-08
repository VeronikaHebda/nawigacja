import numpy as np
from readrnx_studenci import *
from satpos import satpos
from hirvonen import hirvonen
from klobuchar1 import klobuchar
import math as m
import matplotlib.pyplot as plt

def fRneu(fi, lam):
    Rneu = np.array([[-np.sin(fi) * np.cos(lam), -np.sin(lam), np.cos(fi) * np.cos(lam)],
                     [-np.sin(fi) * np.sin(lam), np.cos(lam), np.cos(fi) * np.sin(lam)],
                     [np.cos(fi), 0, np.sin(fi)]]
                    )
    return Rneu

def obrot(xs,ys,zs,a):
    first = np.array([[np.cos(a), np.sin(a), 0],
                      [-np.sin(a), np.cos(a), 0],
                      [0,0,1]])
    second = np.array([xs,ys,zs])
    xs_root = first@second
    return xs_root

def md (el):
    mdel = 1/m.sin(m.radians(m.sqrt((el**2)+6.25)))
    return mdel

def mw (el):
    mwel = 1/m.sin(m.radians(m.sqrt((el**2)+2.25)))
    return mwel

def find_unhealthy(inav, nav):
    ind = nav[:, 30] != 0
    unhealthy_satelites = np.unique(inav[ind])

    return unhealthy_satelites

# scieżka do pliku nawigacyjnego
nav_file = 'WROC00POL_R_20220800000_01D_GN.rnx'
# cieżka do pliku obserwacyjnego
obs_file = 'WROC00POL_R_20220800000_01D_30S_MO.rnx'

# zdefiniowanie czasu obserwacji: daty początkowej i końcowej
# dla pierwszej epoki z pliku będzie to:
time_start = [2022, 3, 21, 0, 0, 0]
time_end = [2022, 3, 21, 23, 59, 59]

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
maska = 10

"""
Przeliczenie daty początkowej i końcowej do sekund tygodnia GPS - niezbędne w celu
poprawnej definicji pętli związanej z czasem obserwacji w ciągu całej doby
"""
week, tow = date2tow(time_start)[0:2]
week_end, tow_end = date2tow(time_end)[0:2]

#usuwanie satelitów
unhealthy_satelites = find_unhealthy(inav, nav)
for i in unhealthy_satelites:
    ind = iobs[:, 0] == i
    iobs = np.delete(iobs, ind, axis=0)
    obs = np.delete(obs, ind, axis=0)

ind_nan = np.isnan(obs[:, 0])
iobs = np.delete(iobs, ind_nan, axis=0)
obs = np.delete(obs, ind_nan, axis=0)


#Obliczenia
omegaE = 7.2921151467 * (10 ** (-5))
dt = 30

alfa = [1.6764e-08,  7.4506e-09, -1.1921e-07,  0.0000e+00]
beta = [1.1059e+05,  0.0000e+00, -2.6214e+05,  0.0000e+00] 
wyniki = []
dop = []
roznicex = []
roznicey = []
roznicez = []
satelity_widoczne = []
x_k = []
y_k = []
z_k = []
T = []


p0= 1013.25#hPa
t0= 291.15#K
Rh0 = 0.5
h_el = 180.818
N = 40.231
h_ort = 140.587
p = p0*(1 - 0.0000226*h_ort)**5.225
temp=t0-0.0065*h_ort
Rh=Rh0*np.exp(-0.0006396*h_ort)
e_= 6.11*Rh*10**(7.5*(temp-273.15)/(temp-35.85))
c1= 77.64
c2=-12.96
c3= 3.718*10**5
Nd0 = c1 * p/temp
Nw0 = c2 * e_/temp + c3 * e_/temp**2
hd= 40136 + 148.72*(temp-273.15)
hw= 11000
dTd0 = (10 ** (-6))/5 * Nd0 * hd
dTw0 = (10 ** (-6))/5 * Nw0 * hw

#dTd0_saas = 0.002277*p
#dTw0_saas = 0.002277 * (1255/temp + 0.05)*e_


for t in range(tow, tow_end+1, dt):
    index = iobs[:, 2] == t
    sats = iobs[index, 0]
    p_obs = obs[index, 0]
    T.append(t)

    dtr = 0
    tau = 0.072
    c = 299792458.0
    tau_list = [0.072] * len(sats)
    for i in range(3):
        #print("Iteracja numer:", i)
        A1 = np.zeros((0, 4))
        y1 = []
        satelity_wid = 0
        for j,sat in enumerate(sats):
            #print("Satelita numer:",sat)
            ind_sat = inav == sat
            nav_sat = nav[ind_sat]
            tr = t - tau_list[j] + dtr
            #print("tau:",tau_list[j])
            xs, ys, zs, dts,dtrel = satpos(nav_sat, week, tr)
            #print("ts,wspolrzedne, dts",tr, xs, ys, zs, dts)
            if i==0:
                a = omegaE * tau
                dtr = 0
            else:
                a = omegaE * tau_list[j]
            xs_root = obrot(xs,ys,zs,a)
            #print("xs root",xs_root)
    
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
            #print("az:",Az)
            #print("el",el)
            #print("r",r)
            
            
            tau_list[j] = r / c
            if el > maska:
                satelity_wid = satelity_wid + 1
                mdel = md(el)
                dTd = dTd0 * mdel
                mwel = mw(el)
                dTw = mwel * dTw0
                dT = dTd + dTw
                #print("dt", dT)
                #zrobienie tego samego dla modelu sastoinen
                #dT_saas = mdel * dTd0_saas + mwel * dTw0_saas
                #print("dT_saas", dT_saas)
                
                dI = klobuchar(t, fi, lam, el, Az, alfa, beta)
                #print(dI)
                #wzbogacenie aplikacji o rozne czestotliwosci, ostatni wzór
                Pcalc = r - c * dts + c * dtr + dT + dI
                #print("pcalc", Pcalc)
                y = Pcalc - p_obs[j]
                y1.append(y)
                A = np.array([[-(xs_root[0] - xr) / r, -(xs_root[1] - yr) / r, -(xs_root[2] - zr) / r, 1]])
                A1 = np.append(A1, A, axis=0)
        licz = satelity_wid
        Q = np.linalg.inv(A1.T @ A1)
        GDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2] + Q[3, 3])
        PDOP = np.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
        TDOP = np.sqrt(Q[3, 3])

        Qneu = Rneu.T @ Q[0:3, 0:3] @ Rneu

        HDOP = np.sqrt(Qneu[0, 0] + Qneu[1, 1])
        VDOP = np.sqrt(Qneu[2, 2])
        PDOP_neu = np.sqrt(Qneu[0, 0] + Qneu[1, 1] + Qneu[2, 2])

        x = - np.linalg.inv(A1.T @ A1) @ A1.T @ y1
        #print("x",x)
        xr = (xr + x[0])
        yr = (yr + x[1])
        zr = (zr + x[2])
        dtr = (dtr + x[3]/c)
        roznicax = xr - 3835751.6257
        roznicay = yr - 1177249.7445
        roznicaz = zr - 4941605.0540

        #print(xr,yr,zr,dtr)
    satelity_widoczne.append(licz)
    wyniki.append([xr,yr,zr])
    x_k.append(xr)
    y_k.append(yr)
    z_k.append(zr)
    roznicex.append(roznicax)
    roznicey.append(roznicay)
    roznicez.append(roznicaz)
    dop.append([GDOP,PDOP,TDOP,HDOP,VDOP])
                    
np.savetxt('wyniki.txt',wyniki, fmt = ['%10.4f','%10.4f','%10.4f'])
x1 = [i for i in range(0, len(T))]
hours = [x for x in range(0, 24)]
labelx = np.arange(0, len(x1), step=120)
#roznice wsp x
fig1 = plt.figure(figsize=(8, 5))
plt.title("Wykres błedów współrzędnych x")
plt.plot(x1,roznicex, color = '#cf2929')
plt.xticks(labelx, hours)
plt.xlabel("[h]")
plt.ylabel("[m]")
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.show()
#roznice wsp y
fig2 = plt.figure(figsize=(8, 5))
plt.title("Wykres błędów współrzędnych y")
plt.plot(x1,roznicey, color = '#50a112')
plt.xticks(labelx, hours)
plt.xlabel("[h]")
plt.ylabel("[m]")
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.show()
#roznice wsp z
fig3 = plt.figure(figsize=(8, 5))
plt.title("Wykres błędów współrzędnych z")
plt.plot(x1,roznicez, color = '#546fcf')
plt.xticks(labelx, hours)
plt.xlabel("[h]")
plt.ylabel("[m]")
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.show()


#odchylenie standardowe
odx = np.std(x_k)
ody = np.std(y_k)
odz = np.std(z_k)
fig6 = plt.figure(figsize=(8, 5))
plt.title("Odchylenie standardowe współrzędnych")
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.bar([1,2,3], [odx,ody,odz], color = '#ffbf00')
plt.xticks([1,2,3], ["x","y","z"])
plt.show()

#statystyki: średni błąd kwadratowy
rmse_x = np.sqrt(np.square(roznicex).mean())
rmse_y = np.sqrt(np.square(roznicey).mean())
rmse_z = np.sqrt(np.square(roznicez).mean())
fig7 = plt.figure(figsize=(8, 5))
plt.title("Średnie błędy kwadratowe współrzędnych")
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.bar([1,2,3], [rmse_x,rmse_y,rmse_z], color = '#bff393')
plt.xticks([1,2,3], ["x","y","z"])
plt.show()

rmse_3D = np.sqrt(rmse_x**2 + rmse_y**2 + rmse_z**2)
#minimalne i maksymalne wspolrzedne
minx = np.min(roznicex)
maxx = np.max(roznicex)
miny = np.min(roznicey)
maxy = np.max(roznicey)
minz = np.min(roznicez)
maxz = np.max(roznicez)

fig8 = plt.figure(figsize=(8, 7))
plt.subplot(2, 1, 2)
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.bar([1,2,3],[minx,miny,minz], color = '#9ac8f4')
plt.title("Minimalne")
plt.xticks([1,2,3], ["x","y","z"])
#plot 2:
plt.subplot(2, 1, 1)
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.bar([1,2,3],[maxx,maxy,maxz], color = '#eaa4c4')
plt.title("Maksymalne")
plt.xticks([1,2,3], ["x","y","z"])
plt.suptitle("Błędy współrzędnych")
plt.show()

# wykres DOP
fig4 = plt.figure(figsize=(8, 5))
plt.title("Współczynniki DOP")
count = 0
for j in range(0, 5):
    dopy = []
    for i in range(0, 2880):
        dopy.append(dop[i][j])
    if count == 0:
        plt.plot(x1, dopy, label="GDOP")
    elif count == 1:
        plt.plot(x1, dopy, label="PDOP")
    elif count == 2:
        plt.plot(x1, dopy, label="TDOP")
    elif count == 3:
        plt.plot(x1, dopy, label="HDOP")
    elif count == 4:
        plt.plot(x1, dopy, label="VDOP")
    count = + 1
plt.xlabel("[h]")
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.legend()
plt.show()
#liczba satel nad maska
fig5 = plt.figure(figsize=(8, 5))
plt.title("Liczba satelitów będących nad maską")
plt.bar(x1, satelity_widoczne, color = '#546fcf')
plt.xlabel("[h]")
plt.xticks(labelx, hours)
plt.grid(color='gray', linestyle='dashed', alpha=0.2)
plt.show()

#napisac w spraku gdzie zmienic maske