#!/usr/bin/python3
from pygnuplot import gnuplot
import  numpy as np

X = np.arange(10)
Y = np.sin(X/(2*np.pi))
Z = Y**2.0

fig1 = gnuplot()
fig1.save([X,Y,Z])
fig1.c('plot "tmp.dat" u 1:2 w 1p')
fig1.c('replot "tmp.dat" u 1:3 w 1p')
fig1.p('myfigure.ps')
