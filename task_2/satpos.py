# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:34:19 2022

@author: Student1
"""

import numpy as np
from datetime import date
import math 


def satpos(nav1, week, tow):

    mu = 3.986005 * (10 ** 14)
    omegaE = 7.2921151467 * (10 ** (-5))

    toe_all = nav1[:, 17] + nav1[:, 27] * 86400 * 7
    roznica = tow - toe_all
    ind = np.argmin(abs(roznica))
    nav0 = nav1[ind,:]

    nav = nav0

    toe = nav[17]

    sqrtA = nav[16]
    e = nav[14]
    i0 = nav[21]
    Omega0 = nav[19]
    ro = nav[23]
    M0 = nav[12]
    delta_n = nav[11]
    Omega_dot = nav[24]
    IDOT = nav[25]
    gps_week = nav[27]
    C_uc = nav[13]
    C_us = nav[15]
    C_ic = nav[18]
    C_is = nav[20]
    C_rc = nav[22]
    C_rs = nav[10]

    af0 = nav[6]
    af1 = nav[7]
    af2 = nav[8]

    tk = tow - toe

    a = sqrtA ** 2

    n0 = math.sqrt(mu / a ** 3)
    n = n0 + delta_n
    Mk = M0 + n * tk
    E1 = Mk
    Ei = Mk + e * np.sin(E1)
    while abs(Ei - E1) >= 10 ** (-12):
        E1 = Ei
        Ei = Mk + e * math.sin(E1)
    Ek = Ei

    Vk = np.arctan2((np.sqrt(1 - e ** 2)) * np.sin(Ek), np.cos(Ek) - e)

    fi_k = Vk + ro

    delta_uk = C_us * np.sin(2 * fi_k) + C_uc * np.cos(2 * fi_k)
    delta_rk = C_rs * np.sin(2 * fi_k) + C_rc * np.cos(2 * fi_k)
    delta_ik = C_is * np.sin(2 * fi_k) + C_ic * np.cos(2 * fi_k)

    uk = fi_k + delta_uk
    rk = a * (1 - e * np.cos(Ek)) + delta_rk
    ik = i0 + IDOT * tk + delta_ik

    xk = rk * np.cos(uk)
    yk = rk * np.sin(uk)

    omega_k = Omega0 + (Omega_dot - omegaE) * tk - (omegaE * toe)

    Xk = xk * np.cos(omega_k) - yk * np.cos(ik) * np.sin(omega_k)
    Yk = xk * np.sin(omega_k) + yk * np.cos(ik) * np.cos(omega_k)
    Zk = yk * np.sin(ik)


    c = 299792458.0  # [m / s]

    dtrel = ((-2 * np.sqrt(mu)) / c ** 2) * e * np.sqrt(a) * np.sin(Ek)
    dts = af0 + af1 * (tow - toe) + af2 * (tow - toe) ** 2 + dtrel
    #return np.array([Xk, Yk, Zk])
    return Xk, Yk, Zk, dts,dtrel


# zajecia 2
# 3835751.6257  1177249.7445  4941605.0540                  APPROX POSITION XYZ

# elif label.find('APPROX POSITION XYZ')!= -1:
    