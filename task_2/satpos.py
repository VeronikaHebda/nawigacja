"""
@author: Weronika Hebda
"""
from readrnx_studenci import readrnxnav, readrnxobs, date2tow
import numpy as np
import math as m

navfile = 'WROC00POL_R_20220800000_01D_GN.rnx'
nav, inav = readrnxnav(navfile)

a = 6378137
e2 = 0.00669438002290

def satpos(nav,week,tow):
    mu = 3.986005 * (10 ** 14)
    we = 7.2921151467 * 10 ** (-5)

    e = nav[14]
    toa = nav[17]
    i = nav[21]
    Idot = nav[25]
    omega_dot = nav[24]
    sqrta = nav[16]
    Omega = nav[19]
    #omega = nav[8]
    M0 = nav[12]
    gps_week = nav[27]
    Cuc = nav[13]
    Cus = nav[15]
    Cic = nav[18]
    Cis = nav[20]
    Crc = nav[22]
    Crs = nav[10]

    # sat = 1
    # ind = inav == sat
    # nav1 = nav[ind, :]
    # week = 2202
    # t = 86400 + 21 * 3600
    # t = t + week * 7 * 86400
    # toe_all = nav1[:, 17] + nav1[:, 27] * 7 * 86400
    # dlt = toe_all - t
    # ind_t = np.argmin(abs(dlt))
    #
    # nav0 = nav1[ind_t, :]

    t = week * 7 * 86400 + tow
    toa_week = gps_week * 7 * 86400 + toa

    #czas, jaki upłynął od epoki wyznaczenia almanachu tk
    tk = t - toa_week

    #dłuższa półoś orbity a
    a = sqrta ** 2

    #ruch średni n
    n = np.sqrt(mu / a ** 3)

    #anomalia średnia Mk
    Mk = M0 + n * tk

    #iteracyjne obliczanie anomalii mimorodowej Ek_end
    Ek = Mk
    while True:
        Eki = Mk + e * np.sin(Ek)
        if abs(Eki - Ek) < 10 ** (-12):
            Ek_end = Eki
            break
        else:
            Ek = Eki

    #anomalia prawdziwa vk
    vk = m.atan2((np.sqrt(1 - e ** 2) * np.sin(Ek_end)), (np.cos(Ek_end) - e))

    phik = vk + omega

    duk = Cus * m.sin(2*phik) + Cuc * m.cos(2*phik)
    drk = Crs * m.sin(2*phik) + Crc * m.cos(2*phik)
    dik = Cis * m.sin(2*phik) + Cic * m.cos(2*phik)

    uk = phik + duk
    rk = a * (1 - e * m.cos(Ek) + drk)
    ik = i + Idot * tk + dik

    xk = rk * np.cos(uk)
    yk = rk * np.sin(uk)

    # #poprawiona długość węzła wstępującego
    omega_k = Omega + (omega_dot - we) * tk - we * toa

    #współrzędne satelity w układzie ECEF
    Xk = xk * np.cos(omega_k) - yk * np.cos(ik) * np.sin(omega_k)
    Yk = xk * np.sin(omega_k) + yk * np.cos(ik) * np.cos(omega_k)
    Zk = yk * np.sin(ik)

    return Xk, Yk, Zk