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

data = [2022,2,25,0,0,0]
week,tow = date2tow(data)
nav = navall[0,:]

xs,ys,zs = satpos(nav,week,tow)
print("wspolrzedne satelity: ",xs,ys,zs)


a = 6378137
e2 = 0.00669438002290

fi = np.deg2rad(52)
lam = np.deg2rad(21)
h = 100

def geo_to_xyz(fi,lam,h):
    N = a/np.sqrt(1-e2*np.sin(fi)**2)
    x = (N + h)* np.cos(fi)*np.cos(lam)
    y = (N + h)* np.cos(fi)*np.sin(lam)
    z = (N*(1-e2)+h)*np.sin(fi)
    return x,y,z

#xr,yr,zr wspolrzedne odbiornika (miejsce obserwacji)
xr,yr,zr = geo_to_xyz(fi, lam, h)
print("wspolrzedne odbiornika: ",xr,yr,zr)


XyzR = np.array([xr,yr,zr])
XyzS = np.array([xs,ys,zs])

XyzSR = XyzS - XyzR
print(XyzSR)

#macierz obrotu
def Rneu(fi,lam):
    Rneu = np.array([[-np.sin(fi)*np.cos(lam),-np.sin(lam),np.cos(fi)*np.cos(lam)],
                [-np.sin(fi)*np.sin(lam),np.cos(lam),np.cos(fi)*np.sin(lam)],
                [np.cos(fi),0,np.sin(fi)] ]             
                )
    return Rneu

Rneu = Rneu(fi,lam)
print(Rneu)
Rneu = Rneu.T

Xsrneu = np.dot(Rneu,XyzSR)
print(Xsrneu)

[n,e,u] = Xsrneu

Az = np.arctan2(e,n)
el = np.arcsin(u/m.sqrt(n**2+e**2+u**2))

print(m.degrees(Az))
print(m.degrees(el))





