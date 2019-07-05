#program to demonstrate constriction factor based particle swarm optimization algorithm
import random
from ctypes import c_byte

import gridgraphdemo as gd
import prim_algorithm as pa
from functools import reduce
import math

class Min_Item:
    def __init__(self, minitem,  item_id):
        self.minitem = minitem
        self.item_id = item_id

class Particle:
    #class used to initialize a pigeon
    def __init__(self, Sx, Sy, V, Xp, Yp):
        self.Sx = Sx
        self.Sy = Sy
        self.V = V
        self.Xp = Xp
        self.Yp = Yp



def constriction_factor_particle_swarm_optimization(objgbest, p, objpbest):
    gbest = math.ceil(1/objgbest)
    pbest = math.ceil(1/objpbest)
    k = 0.729
    Vx = k*(p.V + 2 * random.randint(0,1) * (pbest - p.Xp) + 2 * random.randint (0,1) * (gbest - p.Xp))
    #print(Vx)
    Vy = k*(p.V + 2 * random.randint(0,1) * (pbest - p.Yp) + 2 * random.randint (0,1) * (gbest - p.Yp))
    #print(Vy)
    Vnew = math.ceil((Vx + Vy))//2
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



def get_fitness(Tx, Ty, particle):
    for i in range(len(particle.Sx)):
        if particle.Sx[i] < min(Tx) or particle.Sx[i] > max(Tx):
            continue
        if particle.Sy[i] < min(Ty) or particle.Sy[i] > max(Ty):
            continue
        Tx.append(particle.Sx[i])
        Ty.append(particle.Sy[i])

    distancevector = gd.get_distancevector(Tx, Ty)
    objectivefitness = pa.get_tree(distancevector)
    return objectivefitness

def constriction_factor_particle_swarm_test(Tx, Ty):
    particles = []
    pbestvector = []
    lenTx = len(Tx)
    lenTy = len(Ty)
    # global objfitness
    n = random.randint(0, 10)
    for i in range(n):
        Sx = gd.get_xdata(0, 500, 8)
        Sy = gd.get_ydata(0, 500, 8)
        Xs = reduce((lambda x, y: x + y), Sx) // len(Sx)
        Ys = reduce((lambda x, y: x + y), Sy) // len(Sy)
        particle = Particle(Sx, Sy, 0, Xs, Ys)
        particles.append(particle)
        pbestvector.append(math.inf)
    for i in range(20):
        # objfitness = []

        for j in range(len(particles)):
            mst = get_fitness(Tx, Ty, particles[j])
            if mst < pbestvector[j]:
                pbestvector[j] = mst
            Rx = Tx[0:len(Tx) - lenTx]
            Ry = Tx[0:len(Tx) - lenTy]
            Tx = Tx[0:len(Tx) - len(Rx)]
            Ty = Tx[0:len(Ty) - len(Ry)]
        best_obj_fitness = min(pbestvector)
        for j in range(len(particles)):
            constriction_factor_particle_swarm_optimization(best_obj_fitness, particles[j], pbestvector[j])

    particle_best = particles[pbestvector.index(min(pbestvector))]
    return particle_best


def call_methods(Tx, Ty, lenTx, lenTy):
    # Tx = gd.get_xdata(0, 500, 100)
    # Ty = gd.get_ydata(0, 500, 100)

    lenTx = len(Tx)
    lenTy = len(Ty)

    # Calculating mST for CPSO
    Rx = Tx[0:len(Tx) - lenTx]
    Ry = Ty[0:len(Tx) - lenTy]
    Tx = Tx[0:len(Tx) - len(Rx)]
    Ty = Ty[0:len(Ty) - len(Ry)]
    print("X coordinates =", Tx)
    print("Y coordinates =", Ty)
    bestparticle = constriction_factor_particle_swarm_test(Tx, Ty)
    Rx = Tx[0:len(Tx) - lenTx]
    Ry = Ty[0:len(Ty) - lenTy]
    Tx = Tx[0:len(Tx) - len(Rx)]
    Ty = Ty[0:len(Ty) - len(Ry)]
    # print("Updated X coordinates", Tx)
    # print("Updated Y coordinates", Ty)
    print("X coordinates of best particle", bestparticle.Sx)
    print("Y coordinates of best particle", bestparticle.Sy)
    print("Updated X coordinates", Tx)
    print("Updated Y Coordinates", Ty)
    count = 0
    for i in range(len(bestparticle.Sx)):
        if bestparticle.Sx[i] < min(Tx) or bestparticle.Sx[i] > max(Tx):
            continue
        if bestparticle.Sy[i] < min(Ty) or bestparticle.Sy[i] > max(Ty):
            continue

        Tx.append(bestparticle.Sx[i])
        Ty.append(bestparticle.Sy[i])
        count = count + 1
    print("Updated X Coordinates", Tx)
    print("Updated Y Coordinates", Ty)
    distancevector = gd.get_distancevector(Tx, Ty)
    mst = pa.mst_prim(distancevector)
    mst_size = pa.get_tree(distancevector)
    print("Size of Steiner Tree for Constricted-PSO", mst_size)
    pa.draw_gridgraph(Tx, Ty, mst,lenTx,lenTy)





















