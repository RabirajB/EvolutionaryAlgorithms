import gridgraphdemo as gd
import prim_algorithm as pa
import math
from functools import reduce
import numpy as np

class Weed:
    def __init__(self,Wx,Wy,Xp,Yp,fitness):
        self.Wx = Wx
        self.Wy = Wy
        self.Xp = Xp
        self.Yp = Yp
        self.fitness = fitness

class Seed:
    def __init__(self, Sx, Sy, Xp, Yp):
        self.Sx = Sx
        self.Sy = Sy
        self.Xp = Xp
        self.Yp = Yp
def get_sum(weedlist):
    sum = 0
    for w in weedlist:
        sum = sum+ w.fitness
    return sum

def get_max_fitness(weedlist):
    fmax = 0
    for i in range(len(weedlist)):
        if weedlist[i].fitness > fmax:
            fmax = weedlist[i].fitness
    return fmax

def get_min_fitness(weedlist):
    fmin = 9999
    for i in range(len(weedlist)):
        if weedlist[i].fitness > fmin:
            fmin = weedlist[i].fitness
    return fmin

def get_fitness(Tx,Ty,weed):
    for i in range(len(weed.Wx)):
        if weed.Wx[i] < min(Tx) or weed.Wx[i] > max(Tx):
            continue
        if weed.Wy[i] < min(Ty) or weed.Wy[i] > max(Ty):
            continue
        Tx.append(weed.Wx[i])
        Ty.append(weed.Wy[i])

    distancevector = gd.get_distancevector(Tx, Ty)
    objectivefitness = pa.get_tree(distancevector)
    return objectivefitness

def competitive_exclusion(weedlist):
    meanfitness = get_sum(weedlist) // len(weedlist)
    for weed in weedlist:
        if weed.fitness < meanfitness:
            weedlist.remove(weed)

def iwo_algorithm(Tx,Ty,weedlist,itermax,pmax,Smax,Smin,sigmafinal,sigmainit,n):# n = modulation index
   global fmax,fmin
   lenTx = len(Tx)
   lenTy = len(Ty)
   for i in range(1,itermax+1):
        for w in weedlist:
            w.fitness = (1/get_fitness(Tx,Ty,w))
            Rx = Tx[0:len(Tx) - lenTx]
            Ry = Ty[0:len(Ty) - lenTy]
            Tx = Tx[0:len(Tx) - len(Rx)]
            Ty = Ty[0:len(Ty) - len(Ry)]
        # Convergence
        component = ((itermax - i) / itermax) ** n
        sigmaiter = sigmafinal + (sigmainit - sigmafinal) * component
        fmax = get_max_fitness(weedlist)
        fmin = get_min_fitness(weedlist)
        for weed in weedlist:
            Splant = Smin + math.ceil(weed.fitness * (Smax - Smin)/(fmax - fmin))
            seedlist = []
            # Initiation
            for k in range(Splant):
                Sx = np.random.normal(weed.Xp, sigmaiter, 8) # Skew Position
                print(Sx)
                Sy = np.random.normal(weed.Yp, sigmaiter, 8)
                print(Sy)
                Xp = reduce((lambda x, y: x+y), Sx)//len(Sx)
                Yp = reduce((lambda x, y: x+y), Sy)//len(Sy)
                seed = Seed(Sx, Sy, Xp, Yp)
                seedlist.append(seed)
                #Germination
            for sd in seedlist:
                weed = Weed(sd.Sx, sd.Sy, sd.Xp, sd.Yp, 0)
                fitness = get_fitness(Tx, Ty, weed)
                Rx = Tx[0:len(Tx) - lenTx]
                Ry = Ty[0:len(Ty) - lenTy]
                Tx = Tx[0:len(Tx) - len(Rx)]
                Ty = Ty[0:len(Ty) - len(Ry)]
                weed.fitness = fitness
                weedlist.append(weed)
        # Competetive Exclusion
        if len(weedlist)>pmax:
            competitive_exclusion(weedlist)
   return weedlist

def iwo_test(Tx,Ty):
    lenTx = len(Tx)
    lenTy = len(Ty)
    weedlist=[]
    for i in range(10):
        Wx = gd.get_xdata(0, 500, 8)
        Wy = gd.get_ydata(0, 500, 8)
        Xp = reduce((lambda x,y: x+y),Wx)//len(Wx)
        Yp = reduce((lambda x,y: x+y),Wy)//len(Wy)
        weed = Weed(Wx,Wy,Xp,Yp,0)
        weedlist.append(weed)
    # iwo_algorithm(Tx,Ty,weedlist,itermax,pmax,Smax,Smin,sigmafinal,sigmainit,n)
    wlist = iwo_algorithm(Tx,Ty,weedlist,5,150,10,1,0.01,1,3)
    fmax = get_max_fitness(wlist)
    for weed in wlist:
        if fmax == weed.fitness:
            bestweed = weed
            break
    Rx = Tx[0:len(Tx) - lenTx]
    Ry = Ty[0:len(Ty) - lenTy]
    Tx = Tx[0:len(Tx) - len(Rx)]
    Ty = Ty[0:len(Ty) - len(Ry)]
    print("X-Coordinates of best weed",list(map(lambda x: math.ceil(x),bestweed.Wx)))
    print("Y-Coordinates of best weed",list(map(lambda y: math.ceil(y),bestweed.Wy)))
    count = 0
    bestweed.Wx = list(map(lambda x: math.ceil(x),bestweed.Wx))
    bestweed.Wy = list(map(lambda y: math.ceil(y),bestweed.Wy))
    for i in range(len(bestweed.Wx)):
        if bestweed.Wx[i] < min(Tx) or bestweed.Wx[i] > max(Tx):
            continue
        if bestweed.Wy[i] < min(Ty) or bestweed.Wy[i] > max(Ty):
            continue

        Tx.append(bestweed.Wx[i])
        Ty.append(bestweed.Wy[i])
        count = count + 1
    print("Updated X Coordinates", Tx)
    print("Updated Y Coordinates", Ty)
    distancevector = gd.get_distancevector(Tx, Ty)
    mst = pa.mst_prim(distancevector)
    mst_size = pa.get_tree(distancevector)
    print("Size of Steiner Tree for IWO", mst_size)
    pa.draw_gridgraph(Tx, Ty, mst,lenTx,lenTy)
    Tx = Tx[0:len(Tx) - count]
    Ty = Ty[0:len(Ty) - count]
    print("Restored X Coordinates=", Tx)
    print("Restored Y Coordinates=", Ty)
    print("End of IWO")

Tx = gd.get_xdata(0,500,10)
Ty = gd.get_ydata(0,500,10)
print(Tx)
print(Ty)
lenTx = len(Tx)
lenTy = len(Ty)
print("X Coordinates", Tx)
print("Y Coordinates", Ty)
distancevector = gd.get_distancevector(Tx, Ty)
mst = pa.mst_prim(distancevector)
mst_size = pa.get_tree(distancevector)
print("Size of the MST = ", mst_size)
pa.draw_gridgraph(Tx, Ty, mst, lenTx, lenTy)
iwo_test(Tx,Ty)




