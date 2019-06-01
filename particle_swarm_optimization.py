#program to demonstrate particle swarm optimization algorithm
import random
import gridgraphdemo as gd
import prim_algorithm as pa
from functools import reduce
import math

class Min_Item:
    def __init__(self, minitem,  item_id):
        self.minitem = minitem
        self.item_id = item_id

class Particle:
    #class used to initialize a particle
    def __init__(self, Sx, Sy, V, Xp, Yp):
        self.Sx = Sx
        self.Sy = Sy
        self.V = V
        self.Xp = Xp
        self.Yp = Yp



def particle_swarm_optimization(objgbest, p, objpbest):
    gbest = math.ceil(1/objgbest)
    pbest = math.ceil(1/objpbest)
    Vx = p.V + 2 * random.randint(0,1) * (pbest - p.Xp) + 2 * random.randint(0, 1) * (gbest - p.Xp)
   # print(Vx)
    Vy = p.V + 2 * random.randint(0,1) * (pbest - p.Yp) + 2 * random.randint(0, 1) * (gbest - p.Yp)
   # print(Vy)
    Vnew = (Vx + Vy)//2
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
        Tx.append(particle.Sx[i])
        Ty.append(particle.Sy[i])
    distancevector = gd.get_distancevector(Tx , Ty)
    objfitness = pa.get_tree(distancevector)
    return objfitness

def particle_swarm_test(Tx, Ty):
    particles = []
    pbestvector = []

    #global objfitness
    n = random.randint(0, 10)
    for i in range(n):
        Sx = gd.get_xdata(0, 500, 98)
        Sy = gd.get_ydata(0, 500, 98)
        Xs = reduce((lambda x, y: x+y), Sx) // len(Sx)
        Ys = reduce((lambda x, y: x+y), Sy) // len(Sy)
        particle = Particle(Sx, Sy, 0, Xs, Ys)
        particles.append(particle)
        pbestvector.append(math.inf)
    for i in range(20):
        #objfitness = []

        for j in range(len(particles)):
            mst = get_fitness(Tx, Ty, particles[j])
            if mst < pbestvector[j]:
                pbestvector[j] = mst
            Tx = Tx[0:len(Tx) - len(particles[j].Sx)]
            Ty = Ty[0:len(Ty) - len(particles[j].Sy)]
        best_obj_fitness = min(pbestvector)
        for j in range(len(particles)):
            particle_swarm_optimization(best_obj_fitness, particles[j], pbestvector[j])
            print("X Coordinates",particles[j].Sx)
            print("Y Coordinates",particles[j].Sy)
    particle_best = particles[pbestvector.index(min(pbestvector))]
    return particle_best












 







