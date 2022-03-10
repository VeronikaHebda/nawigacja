from read_yuma import read_yuma
import numpy as np 
from date2tow import date2tow

alm = 'almanac.yuma.week0150.589824.txt'
navall = read_yuma(alm)

data = [2022,2,25,0,0,0]
week,tow = date2tow(data)
print(week,tow)

nav = navall[0,:]
mu = 3.986005 * (10 ** 14)
we = 7.2921151467*10**(-5)

prn = nav[0]
e = nav[2]
toa = nav[3]
i = nav[4]
omega_dot = nav[5]
sqrta = nav[6]
Omega = nav [7]
omega = nav [8]
M0 = nav[9]
gps_week = nav[12]

t = week * 7 * 86400 + tow
toa_week = gps_week * 7 * 86400 + toa

tk = t - toa_week
print(tk)

a = sqrta**2
n = np.sqrt(mu/a**3)

Mk = M0 + n*tk
Ek = Mk
while True:
    Eki = Mk + e*np.sin(Ek)
    if abs(Eki - Ek) < 10**(-12):
        Ek_end = Eki
        break
    else:
        Ek = Eki

vk = np.arctan2((np.sqrt(1-e**2) * np.sin(Ek_end)),(np.cos(Ek_end)-e))

fi = vk + omega