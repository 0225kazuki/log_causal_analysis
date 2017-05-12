# -*- coding: utf-8 -*-
from scipy import arange, hamming, sin, pi
from scipy.fftpack import fft, ifft, fftfreq
import matplotlib.pyplot as plt
import search_burst as sb
import numpy as np
import pandas as pd
import sys
import datetime

event = sb.open_dump(sys.argv[1])
day = sys.argv[2]
ev_year = int(day[:4])
ev_month = int(day[4:6])
ev_day = int(day[6:8])

ev_date = datetime.date(ev_year,ev_month,ev_day)
plot_data = [row.time() for row in event if row.date() == ev_date]
ev_data = [row.hour*3600 + row.minute*60 + row.second for row in plot_data]

fs = 1 # Sampling rate
L = 2**16 # Signal length

x = [10. if i in ev_data else  0. for i in range(L)]

# test data
# x = [10. if i%3600 == 0 else  0. for i in range(L)]

# # 440[Hz]のサイン波を作る。
# sine_440 = sin(2. * pi * arange(L) * 440. / fs)
# # 600[Hz]のサイン波を作る。
# sine_600 = 2 * sin(2. * pi * arange(L) * 600. / fs)
# # 800[Hz]のサイン波を作る。
# sine_800 = 3 * sin(2. * pi * arange(L) * 800. / fs)
#
# # 全部足す
# sig = sine_440 + sine_600 + sine_800
#
# print(sig);exit()

# 窓関数
win = hamming(L)

# # フーリエ変換
# spectrum_nw = fft(sig) # 窓関数なし
# spectrum = fft(sig * win) # 窓関数あり
# half_spectrum_nw = abs(spectrum_nw[: L / 2 + 1])
# half_spectrum = abs(spectrum[: L / 2 + 1])

spectrum = fft(x * win)
freq = fftfreq(L,fs)
half_spectrum = abs(spectrum[1:int(L / 2)])


# # フーリエ逆変換
# resyn_sig = ifft(spectrum)
# resyn_sig /= win

# 図を表示
fig = plt.figure(figsize=(10,10))
fig.add_subplot(211)
plt.plot(x)
plt.xlim([0, L])
plt.title("1. Input signal", fontsize = 20)
fig.add_subplot(212)
# plt.plot(half_spectrum)
plt.plot(freq[1:int(L/2)], half_spectrum)
plt.xlim([0, 10**(-3)])
# plt.xscale('log')
plt.title("2. Spectrum (no window)", fontsize = 20)

plt.savefig('fft.png')
