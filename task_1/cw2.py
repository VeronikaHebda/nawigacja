# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:22:52 2022

@author: Student1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:47:45 2022

@author: Student1
"""

from read_yuma import read_yuma
import numpy as np 
import math as m
from date2tow import date2tow
from satpos import satpol

alm = 'almanac.yuma.week0150.589824.txt'
navall = read_yuma(alm)

data = [2022,2,25,0,0,0]
week,tow = date2tow(data)
nav = navall[0,:]

xs,ys,zs = satpol(nav)
print("wspolrzedne satelity: ",xs,ys,zs)


a = 6378137
e2 = 0.00669438002290

fi = np.deg2rad(52)
lam = np.deg2rad(21)
h = 100
#xr wspolrzedne odbiornika (miejsce obserwacji)

def geo_to_xyz(fi,lam,h):
    N = a/np.sqrt(1-e2*np.sin(fi)**2)
    x = (N + h)* np.cos(fi)*np.cos(lam)
    y = (N + h)* np.cos(fi)*np.sin(lam)
    z = (N*(1-e2)+h)*np.sin(fi)
    return x,y,z

xr,yr,zr = geo_to_xyz(fi, lam, h)
print("wspolrzedne odbiornika: ",xr,yr,zr)
    
#for sat in nav:
 #   xs = satpos(sat,week,t)
  #  xsr = xs - xr

XyzR = np.array([xr,yr,zr])
XyzS = np.array([xs,ys,zs])

XyzSR = XyzR - XyzS
print(XyzSR)

def Rneu(fi,lam):
    Rneu = np.array([[-np.sin(fi)*np.cos(lam),-np.sin(fi),np.cos(fi)*np.cos(lam)],
                [-np.sin(fi)*np.sin(lam),np.cos(fi),np.cos(fi)*np.sin(lam)],
                [np.cos(fi),0,np.sin(fi)] ]             
                )
    return Rneu

Rneu = Rneu(fi,lam)






