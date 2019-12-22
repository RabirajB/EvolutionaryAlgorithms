import random
import matplotlib.pyplot as plot
from numpy import array, arange
from numpy.random import randint
import math

def get_xdata(start, end, num):
    '''x = []
    for _ in range(num):
        x.append(random.randint(start, end))'''
    
    return randint(start, end, num)

def get_ydata(start, end, num):
    '''y = []
    for _ in range(num):
        y.append(random.randint(start, end))'''
   
    return randint(start, end, num)

def display_grid():
    x = get_xdata(20, 30, 10)
    y = get_ydata(20, 30, 10)
    fig = plot.figure()
    ax = fig.gca()
    ax.set_xticks(arange(0, 501, 1))
    ax.set_yticks(arange(0, 501, 1))
    plot.scatter(x, y)
    plot.grid()
    plot.show()

def get_distancevector(Tx,Ty):

    distance = []
    distvector = []
    for i in range(len(Tx)):
        x = Tx[i]
        y = Ty[i]
        for j in range(len(Tx)):

            #print("Difference between x-coordinates=", abs(x - Tx[j]))
            #print("Difference between y-coordinates=", abs(y - Ty[j]))
            d = abs(x - Tx[j]) + abs(y - Ty[j])
            #print("Distance=", d)
            if(d == 0):
                distance.append(math.inf)
            else:
                distance.append(d)
        distvector.append(distance)
        distance = []
    return distvector

'''def  draw_gridgraph(start, end, n):
    Sx = get_xdata(start, end, n)
    Sy = get_ydata(start, end, n)
    fig = plot.figure()
    ax = fig.gca()
    ax.set_xticks(arange(0, 501, 1))
    ax.set_yticks(arange(0, 501, 1))
    for i in range(len(Sx)):
        if i+1 == len(Sx):
            break
        else:
            destx = Sx[i+1]
            desty = Sy[i+1]
            #figure_plot(Sx[i], Sy[i], destx, desty)
    plot.show()'''

def figure_plot(x, y, destx, desty, a, b, lenTx,lenTy):
    term_pts = plot.scatter(x, y, c='r', marker='o')
    str_pts = plot.scatter(destx, desty, c='b', marker='s')
    if a < lenTx :
        plot.plot(x, y,"ro")
    if b < lenTx:
        plot.plot(destx, desty,"ro")
    if a>=lenTx:
        plot.plot(x,y,"bs", label='Steiner Points')
    if b >= lenTx:
        plot.plot(destx,desty,"bs", label='Steiner Points')
    plot.plot([x, destx], [y, y], color='black')
    plot.plot([destx, destx], [y, desty], color = 'black')
    return (term_pts, str_pts)