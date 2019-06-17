# program to demonstrate pigeon optimization algorithm
import random
import gridgraphdemo as gd
import prim_algorithm as pa
from functools import reduce
import math


class Pigeon:
    # class used to initialize a pigeon
    def __init__(self, Sx, Sy, V, Xp, Yp):
        self.Sx = Sx
        self.Sy = Sy
        self.V = V
        self.Xp = Xp
        self.Yp = Yp


def pigeon_optimization(Objbest, p, iteration):
    fitnessbest = math.ceil(1 / Objbest)
    Vx = p.V * math.e ** (random.randint(0, 1) * iteration) + random.randint(0, 1) * (fitnessbest - p.Xp)
    # print("x velocity=",Vx)
    Vy = p.V * math.e ** (random.randint(0, 1) * iteration) + random.randint(0, 1) * (fitnessbest - p.Yp)
    # print("Y velocity",Vy)
    Vnew = math.ceil((Vx + Vy)) // 2
    p.V = Vnew

    Sxnew = list(map(lambda x: x + Vx, p.Sx))
    Synew = list(map(lambda y: y + Vy, p.Sy))
    Xpnew = reduce((lambda x, y: x + y), Sxnew) // len(p.Sx)
    Ypnew = reduce((lambda x, y: x + y), Synew) // len(p.Sy)
    if Xpnew < 0 or Xpnew > 500 or Ypnew < 0 or Ypnew > 500:
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
        if pigeon.Sx[i] < min(Tx) or pigeon.Sx[i] > max(Tx):
            continue
        if pigeon.Sy[i] < min(Ty) or pigeon.Sy[i] > max(Ty):
            continue
        Tx.append(pigeon.Sx[i])
        Ty.append(pigeon.Sy[i])

    distancevector = gd.get_distancevector(Tx, Ty)
    objectivefitness = pa.get_tree(distancevector)
    return objectivefitness


def pigeon_test(Tx, Ty):
    pigeons = []
    global objfitness
    n = random.randint(0, 10)
    lenTx = len(Tx)
    lenTy = len(Ty)
    for i in range(n):
        Sx = gd.get_xdata(0, 500, 98)
        Sy = gd.get_ydata(0, 500, 98)
        Xs = reduce((lambda x, y: x + y), Sx) // len(Sx)
        Ys = reduce((lambda x, y: x + y), Sy) // len(Sy)
        pigeon = Pigeon(Sx, Sy, 0, Xs, Ys)
        pigeons.append(pigeon)

    for i in range(20):
        objfitness = []
        for j in range(len(pigeons)):
            mst = get_fitness(Tx, Ty, pigeons[j])
            objfitness.append(mst)
            Rx = Tx[0:len(Tx) - lenTx]
            Ry = Tx[0:len(Tx) - lenTy]
            Tx = Tx[0:len(Tx) - len(Rx)]
            Ty = Tx[0:len(Ty) - len(Ry)]
            # Tx = Tx[0:len(Tx) - len(pigeons[j].Sx)]
            # print(Tx)
            # Ty = Ty[0:len(Ty) - len(pigeons[j].Sy)]
            # print(Ty)
        best_obj_fitness = min(objfitness)

        for j in range(len(pigeons)):
            pigeon_optimization(best_obj_fitness, pigeons[j], i)

    pigeon_best = pigeons[objfitness.index(min(objfitness))]
    print(pigeon_best.Sx)
    print(pigeon_best.Sy)
    return pigeon_best


def call_methods(Tx, Ty, lenTx, lenTy):
    # Tx = gd.get_xdata(0, 500, 10)
    # Ty = gd.get_ydata(0, 500, 10)
    '''
    lenTx = len(Tx)
    lenTy = len(Ty)
    '''
    # Calculating mST for PIO
    print("X coordinates =", Tx)
    print("Y coordinates =", Ty)
    bestpigeon = pigeon_test(Tx, Ty)
    Rx = Tx[0:len(Tx) - lenTx]
    Ry = Ty[0:len(Ty) - lenTy]
    Tx = Tx[0:len(Tx) - len(Rx)]
    Ty = Ty[0:len(Ty) - len(Ry)]
    # print("Updated X coordinates", Tx)
    # print("Updated Y coordinates", Ty)
    print("X coordinates of best pigeon", bestpigeon.Sx)
    print("Y coordinates of best pigeon", bestpigeon.Sy)
    print("Updated X coordinates", Tx)
    print("Updated Y Coordinates", Ty)
    count = 0
    for i in range(len(bestpigeon.Sx)):
        if bestpigeon.Sx[i] < min(Tx) or bestpigeon.Sx[i] > max(Tx):
            continue
        if bestpigeon.Sy[i] < min(Ty) or bestpigeon.Sy[i] > max(Ty):
            continue

        Tx.append(bestpigeon.Sx[i])
        Ty.append(bestpigeon.Sy[i])
        count = count + 1
    print("Updated X Coordinates", Tx)
    print("Updated Y Coordinates", Ty)
    distancevector = gd.get_distancevector(Tx, Ty)
    mst = pa.mst_prim(distancevector)
    mst_size = pa.get_tree(distancevector)
    print("Size of Steiner Tree for PIO", mst_size)
    pa.draw_gridgraph(Tx, Ty, mst)
    Tx = Tx[0:len(Tx) - count]
    Ty = Ty[0:len(Ty) - count]
    print("Restored X Coordinates=", Tx)
    print("Restored Y Coordinates=", Ty)
    print("End of PIO")
