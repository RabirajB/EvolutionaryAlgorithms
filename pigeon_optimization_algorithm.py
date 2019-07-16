# program to demonstrate pigeon optimization algorithm
import random
import gridgraphdemo as gd
import prim_algorithm as pa
from functools import reduce
import math
import numpy as np # changes done


class Pigeon:
    # class used to initialize a pigeon
    def __init__(self, Sx, Sy, V, Xp, Yp,fitness):
        self.Sx = Sx
        self.Sy = Sy
        self.V = V
        self.Xp = Xp
        self.Yp = Yp
        self.fitness = fitness
        


def pigeon_optimization_map_and_compass(fitnessbest, p, iteration):

    Vx = p.V * math.e ** (random.randint(0, 1) * iteration) + random.randint(0, 1) * (fitnessbest - p.Xp)
    Vy = p.V * math.e ** (random.randint(0, 1) * iteration) + random.randint(0, 1) * (fitnessbest - p.Yp)
    Vnew = math.ceil((Vx + Vy)) // 2 
    p.V = Vnew

    #Sxnew = list(map(lambda x: x + Vx, p.Sx))
    #Synew = list(map(lambda y: y + Vy, p.Sy))
    #Xpnew = reduce((lambda x, y: x + y), Sxnew) // len(p.Sx)
    #Ypnew = reduce((lambda x, y: x + y), Synew) // len(p.Sy)

    Sxnew = p.Sx + Vx # changes done
    Synew = p.Sy + Vy # changes done
    length = p.Sx.size # changes done
    Xpnew = np.sum(Sxnew) // length # changes done
    Ypnew = np.sum(Synew) // length # changes done

    if Xpnew < 0 or Xpnew > 500 or Ypnew < 0 or Ypnew > 500:
        #p.Sx = p.Sx
        #p.Sy = p.Sy
        p.V = p.V
        #p.Xp = p.Xp
        #p.Yp = p.Yp
    else:
        p.Sx = Sxnew
        p.Sy = Synew
        p.V = Vnew
        p.Xp = Xpnew
        p.Yp = Ypnew


def get_fitness(Tx, Ty, pigeon):
    for i in range(pigeon.Sx.size):
        if pigeon.Sx[i] < min(Tx) or pigeon.Sx[i] > max(Tx):
            continue
        if pigeon.Sy[i] < min(Ty) or pigeon.Sy[i] > max(Ty):
            continue
        np.append(Tx, pigeon.Sx[i])
        np.append(Ty, pigeon.Sy[i])

    distancevector = gd.get_distancevector(Tx, Ty)
    objectivefitness = pa.get_tree(distancevector)
    return objectivefitness

def calculate_sum_positionsX(pigeons):
    sumX,sumx = 0,0
    for i in range(len(pigeons)):
        sumx += pigeons[i].fitness
        sumX += (pigeons[i].Xp)*pigeons[i].fitness
    return sumX,sumx

def calculate_sum_positionsY(pigeons):
    sumY,sumy = 0,0
    for i in range(len(pigeons)):
        sumy += pigeons[i].fitness
        sumY += (pigeons[i].Yp)*pigeons[i].fitness
    return sumY,sumy

def calculate_x_position(Sx,Xxc):
    for i in range(len(Sx)):
        temp = Sx[i] + random.randint(0,1) * (Xxc - Sx[i])
        Sx[i] = temp

def calculate_y_position(Sy,Yyc):
    for i in range(len(Sy)):
        Sy[i] = Sy[i] + random.randint(0,1) * (Yyc - Sy[i])

def pigeon_test(Tx, Ty):
    pigeons = []
    #global objfitness
    #n = random.randint(0, 10)
    lenTx = len(Tx)
    lenTy = len(Ty)
    for i in range(150):
        Sx = gd.get_xdata(0, 500, lenTx - 2)
        Sy = gd.get_ydata(0, 500, lenTy - 2)
        len_S = Sx.size
        #Xs = reduce((lambda x, y: x + y), Sx) // len(Sx)
        #Ys = reduce((lambda x, y: x + y), Sy) // len(Sy)
        Xs = np.sum(Sx) // len_S
        Ys = np.sum(Sy) // len_S
        pigeon = Pigeon(Sx, Sy, 0, Xs, Ys,0)
        pigeons.append(pigeon)

    for i in range(10):

        for j in range(len(pigeons)):
            mst = get_fitness(Tx, Ty, pigeons[j])
            pigeons[j].fitness = 1/mst
            Rx = Tx[0:len(Tx) - lenTx]
            Ry = Tx[0:len(Tx) - lenTy]
            Tx = Tx[0:len(Tx) - len(Rx)]
            Ty = Tx[0:len(Ty) - len(Ry)]
            # Tx = Tx[0:len(Tx) - len(pigeons[j].Sx)]
            # print(Tx)
            # Ty = Ty[0:len(Ty) - len(pigeons[j].Sy)]
            # print(Ty)

        best_fitness = max(pigeons, key = lambda pigeon: pigeon.fitness).fitness

        for j in range(len(pigeons)):
            pigeon_optimization_map_and_compass(best_fitness, pigeons[j], i)
    pigeon_optimization_landmark(Tx,Ty,lenTx,lenTy,pigeons)
    pigeon_best = max(pigeons, key = lambda pigeon: pigeon.fitness)
    print(pigeon_best.Sx)
    print(pigeon_best.Sy)
    return pigeon_best

def pigeon_optimization_landmark(Tx, Ty, lenTx, lenTy, pigeons):

    for i in range(len(pigeons),10, - math.ceil(len(pigeons)//2)):
        pigeons = pigeons[0:i]
        pigeons.sort(key=lambda pigeon: pigeon.fitness, reverse=True)
        sumX,sumx = calculate_sum_positionsX(pigeons)
        sumY,sumy = calculate_sum_positionsY(pigeons)
        Xxc = sumX // (i*sumx)
        Yyc = sumY // (i*sumy)
        for j in range(len(pigeons)):

            #Sxnew = list(map(lambda x: x - random.randint(0,1)*(Xxc - x), pigeons[j].Sx))
            #Synew = list(map(lambda y: y - random.randint(0,1)*(Yyc - y), pigeons[j].Sy))
            Sxnew = pigeons[j].Sx - (random.randint(0, 1)*(Xxc - pigeons[j].Sx))
            Synew = pigeons[j].Sy - (random.randint(0, 1)*(Yyc - pigeons[j].Sy))
            #calculate_x_position(Sxnew,Xxc)
            #calculate_y_position(Synew,Yyc)
            len_S = pigeons[j].Sx.size
            #Xpnew = reduce((lambda x, y: x + y), Sxnew) // len(pigeons[j].Sx)
            #Ypnew = reduce((lambda x, y: x + y), Synew) // len(pigeons[j].Sy)
            Xpnew = np.sum(pigeons[j].Sx) // len_S
            Ypnew = np.sum(pigeons[j].Sy) // len_S

            if Xpnew < 0 or Xpnew > 500 or Ypnew < 0 or Ypnew > 500:
                '''pigeons[j].Sx = pigeons[j].Sx
                pigeons[j].Sy = pigeons[j].Sy
                pigeons[j].V = pigeons[j].V
                pigeons[j].Xp = pigeons[j].Xp
                pigeons[j].Yp = pigeons[j].Yp'''
                pass
            else:
                pigeons[j].Sx = Sxnew
                pigeons[j].Sy = Synew
                pigeons[j].Xp = Xpnew
                pigeons[j].Yp = Ypnew
                pigeons[j].fitness = 1/get_fitness(Tx,Ty,pigeons[j])
                Rx = Tx[0:len(Tx) - lenTx]
                Ry = Ty[0:len(Ty) - lenTy]
                Tx = Tx[0:len(Tx) - len(Rx)]
                Ty = Ty[0:len(Ty) - len(Ry)]

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

        #Tx.append(math.floor(bestpigeon.Sx[i]))
        #Ty.append(math.floor(bestpigeon.Sy[i]))
        np.append(Tx, np.floor(bestpigeon.Sx[i]))
        np.append(Ty, np.floor(bestpigeon.Sy[i]))
        count = count + 1
    print("Updated X Coordinates", Tx)
    print("Updated Y Coordinates", Ty)
    distancevector = gd.get_distancevector(Tx, Ty)
    mst = pa.mst_prim(distancevector)
    mst_size = pa.get_tree(distancevector)
    print("Size of Steiner Tree for PIO", mst_size)
    pa.draw_gridgraph(Tx, Ty, mst, lenTx, lenTy)
    Tx = Tx[0:len(Tx) - count]
    Ty = Ty[0:len(Ty) - count]
    print("Restored X Coordinates=", Tx)
    print("Restored Y Coordinates=", Ty)
    print("End of PIO")
