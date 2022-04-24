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
el_mask = 10  # elevation mask/cut off in degrees

"""
Przeliczenie daty początkowej i końcowej do sekund tygodnia GPS - niezbędne w celu
poprawnej definicji pętli związanej z czasem obserwacji w ciągu całej doby
"""
week, tow = date2tow(time_start)[0:2]
week_end, tow_end = date2tow(time_end)[0:2]

# %% Obliczenia
omegaE = 7.2921151467 * (10 ** (-5))
dt = 30
for t in range(tow, tow_end+1, dt):
    # %% Obliczenia

    # sats = iobs[ind_t, 0]
    # obs_t = obs[ind_t, :]
    #
    # tau = 0.072
    # for sat in sats:
    #     ind_sat = invav == sat
    #     nav_sat = nav[ind_sat]
    #
    #     tr = t - tau + dtr
    #     xs, dts = satpos(ts, week, nav_sat)

    index = iobs[:, 2] == t
    sats = iobs[index, 0]
    p_obs = obs[index, 0]


dtr = 0
tau = 0.072
c = 299792458.0
for i in range(5):
    for sat in sats:
        print(sat)
        ind_sat = inav == sat
        nav_sat = nav[ind_sat]
        tr = 86400 - tau + dtr

        xs, ys, zs, dts,dtr = satpos(nav_sat, week, tr)
        print(tr, xs, ys, zs, dtr)
        if sat==1:
            a = omegaE * tau
            dtr = 0
        else:
            a = omegaE * r/c
        xs_root = obrot(xs,ys,zs,a)
        print(xs_root)

        fi,lam,h = hirvonen(xr,yr,zr)
        XyzR = np.array([xr, yr, zr])
        XyzS = np.array([xs_root[0], xs_root[1], xs_root[2]])
        XyzSR = XyzS - XyzR
        Rneu = fRneu(fi, lam)
        Rneu2 = Rneu.T
        Xsrneu = np.dot(Rneu2, XyzSR)
        [n, e, u] = Xsrneu

        # elewacja i azymut jednego satelity w jednej godzinie
        Az = np.arctan2(e, n)
        Az = m.degrees(Az)
        el = np.arcsin(u / m.sqrt(n ** 2 + e ** 2 + u ** 2))
        el = m.degrees(el)
        r = np.linalg.norm(XyzSR)
        print(Az)
        print(el)
        print(r)
        print(dts,dtr)
        #if el > maska: to potem
        Pcalc = r - c*dts + c*dtr
        print(Pcalc)


"""
Otwieramy dużą pętlę
for t in range(tow, tow_end+1, dt): gdzie dt równe 30
    Wewnątrz tej pętli, zajmujemy się obserwacjami wyłącznie dla jednej epoki (epoka t), zatem:
        1. Wybieramy obserwacje dla danej epoki, na podstawie tablicy iobs oraz naszej epoki t
        czyli, wybieramy te obserwacje z tablicy obs, dla których w tablicy iobs ostatnia kolumna 
        jest równa t - zmienna Pobs
        2. wybieramy satelity, obserwowane w danej epoce, na podstawie tablicy iobs - na podstawie 
        naszego t - zmienna sats
        3. Definiujemy wartosci przybliżone: współrzędne odbiornika xr oraz błąd zegara odbiornika
        dtr = 0 oraz czasu propagacji sygnału tau = 0.072
        4. Najprawdopodobniej przyda się definicja pustych wektorów, np. zawierających 
        odległosci geometryczne (wartoci przybliżone na podstawie tau) lub 

    Przechodzimy do iteracyjnych obliczeń współrzędnych odbiornika:
        pętla for (lub while), do testowania programu przyjmujemy pętle for dla 5 iteracji
        Po weryfikacji działania programu, można zamienić pętlę for na pętle while, dopisując
        warunek zbieżnoci kolejnych współrzędnych - skróci nam to czas obliczeń, ponieważ w 
        praktyce nie potrzeba jest nam 5 iteracji, ale najczęciej 3

        for i in range(5):
            Wykonujemy kolejne obliczenia, niezależnie dla kolejnych satelitów, obserwowanych
            w danej epoce, czyli przechodzimy do pętli:
                for sat in sats: (przyda nam się tutaj również indeks satelity, więc byłoby
                                  to co np. for i, sat in enumerate(sats):)
                    Obliczamy czas emisji sygnału:
                        tr = t - tau + dtr
                    Kolejne kroki, znane z poprzedniego ćwiczenia:
                    wyznaczamy współrzędne satelity xs (oraz błąd zegara satelity dts) na czas tr (UWAGA, w kolejnych iteracjach
                    czas tr będzie się zmieniał i aktualizował, neizależnie dla każdego satelity)

                    Odległosć geometryczna:
                        1. rotacja do układu chwilowego - otrzymujemy xs_rot
                        2. Na podstawie xs_rot obliczamy odległosć geometryczną rho

                    Obliczamy elewację i azymut
                    Macierz Rneu definiujemy na podstawie xr, przeliczonego do współrzędnych
                    phi lambda, algorytmem Hirvonena

                    Odrzucamy satelity znajdujące się poniżej maski

                    Obliczamy poprawki atmosferyczne:
                        trop oraz iono

                    Wyznaczamy pseudoodległosć przybliżoną (obliczoną), jako:
                        Pcalc = rho - cdts + dtr + trop + iono

                    Wyznaczamy kolejen elementy wektora wyrazów wolnych y, jako:
                        y = Pcalc - Pobs

                    Budujemy kolejne wiersze macierzy A:

                Kończymy pętle dla kolejnych satelitów

                1. Łączymy ze sobą elementy wektora wyrazów wolych w jeden wektor
                2. Łączymy ze sobą kolejnę wiersze macierz współczynników A
                3. Rozwiązujemy układ równać, metodą najmniejszych kwadratów

                x = -np.linalg.inv(A.T@A) @ (A.T @ y)

                gdzie x jest wektorem zawierającym szukane przyrosty do niewiadomych

                Aktualizujemy wartosci przybliżone o odpowiednie elementy wektora x
                xr[0] = xr[0] + x[0]
                xr[1] = xr[1] + x[1]
                xr[2] = xr[2] + x[2]
                dtr = dtr + x[3]/c 

                Tak obliczone wartoci xr oraz dtr stanowią wartoci wejsciowe do kolejnej iteracji, itd 
                do skończenia piątej iteracji lub spełnienia warunku zbieżnoci współrzędncyh


            Po skończeniu 5. iteracji, zbieramy obliczone współrzędne xr - warto zebrać również
            liczby obserwowanych satelitów, obliczone wartoci współczynników DOP (przynajmniej PDOP)

"""