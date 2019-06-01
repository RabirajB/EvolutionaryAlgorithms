#program to demonstrate pigeon optimization algorithm
import random
import gridgraphdemo as gd
import prim_algorithm as pa
from functools import reduce
import math

class Min_Item:
    def __init__(self, minitem,  item_id):
        self.minitem = minitem
        self.item_id = item_id

class Pigeon:
    #class used to initialize a pigeon
    def __init__(self,Sx,Sy,V,Xp,Yp):
        self.Sx = Sx
        self.Sy = Sy
        self.V = V
        self.Xp = Xp
        self.Yp = Yp

def get_min_item(arr):
    min = math.inf
    index = 0
    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i]
            index = i
    item = Min_Item(min, index)
    return item

def pigeon_optimization(Objbest,p,iteration):
    fitnessbest = math.ceil(1/Objbest)
    Vx = p.V * math.e**(random.randint(0,1)*iteration) + random.randint(0, 1) * (fitnessbest- p.Xp)
    #print("x velocity=",Vx)
    Vy = p.V * math.e**(random.randint(0,1)*iteration) + random.randint(0, 1) * (fitnessbest- p.Yp)
    #print("Y velocity",Vy)
    Vnew = math.ceil((Vx + Vy))//2
    p.V = Vnew

    Sxnew = list(map(lambda x: x + Vx, p.Sx))
    Synew = list(map(lambda y: y + Vy, p.Sy))
    Xpnew = reduce((lambda x, y: x + y), Sxnew) // len(p.Sx)
    Ypnew = reduce((lambda x, y: x + y), Synew) // len(p.Sy)
    if Xpnew < 0 or  Ypnew < 0 :
        p.Sx = p.Sx
        p.Sy = p.Sy
        p.V = p.V
        p.Xp = p.Xp
        p.Yp = p.Yp
    else:
        p.Sx = Sxnew
        p.Sy = Synew
        p.V = Vnew
        p.Xp = Xpnew
        p.Yp = Ypnew

def get_fitness(Tx, Ty, pigeon):
    for i in range(len(pigeon.Sx)):
        Tx.append(pigeon.Sx[i])
        Ty.append(pigeon.Sy[i])
    distancevector = gd.get_distancevector(Tx, Ty)
    objectivefitness = pa.get_tree(distancevector)
    return objectivefitness

def pigeon_test(Tx,Ty):
    pigeons = []
    global objfitness
    n = random.randint(0,10)
    for i in range(n):
        Sx = gd.get_xdata(0, 500, 98)
        Sy = gd.get_ydata(0, 500, 98)
        Xs = reduce((lambda x,y: x+y), Sx) // len(Sx)
        Ys = reduce((lambda x,y: x+y), Sy) // len(Sy)
        pigeon = Pigeon(Sx, Sy, 0, Xs, Ys)
        pigeons.append(pigeon)

    for i in range(20):
        objfitness = []
        for j in range(len(pigeons)):

            mst = get_fitness(Tx, Ty, pigeons[j])
            objfitness.append(mst)
            Tx = Tx[0:len(Tx) - len(pigeons[j].Sx)]
            #print(Tx)
            Ty = Ty[0:len(Ty) - len(pigeons[j].Sy)]
            #print(Ty)
        best_obj_fitness = min(objfitness)

        for j in range(len(pigeons)):

            pigeon_optimization(best_obj_fitness, pigeons[j], i)

    pigeon_best = pigeons[objfitness.index(min(objfitness))]
    print(pigeon_best.Sx)
    print(pigeon_best.Sy)
    print(Tx)
    print(Ty)
    return pigeon_best






















