"""
@author: Weronika Hebda
"""

import numpy as np
import math as m

def satpos(nav,week,tow):
    mu = 3.986005 * (10 ** 14)
    we = 7.2921151467 * 10 ** (-5)

    e = nav[2]
    toa = nav[3]
    i = nav[4]
    omega_dot = nav[5]
    sqrta = nav[6]
    Omega = nav[7]
    omega = nav[8]
    M0 = nav[9]
    gps_week = nav[12]

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

    t = vk + omega
    #promien orbity rk
    rk = a * (1 - e * np.cos(Ek_end))
    #współrzędne satelity w układzie orbity
    xk = rk * np.cos(t)
    yk = rk * np.sin(t)

    #poprawiona długość węzła wstępującego
    omega_k = Omega + (omega_dot - we) * tk - we * toa

    #współrzędne satelity w układzie ECEF
    Xk = xk * np.cos(omega_k) - yk * np.cos(i) * np.sin(omega_k)
    Yk = xk * np.sin(omega_k) + yk * np.cos(i) * np.cos(omega_k)
    Zk = yk * np.sin(i)

    return Xk, Yk, Zk