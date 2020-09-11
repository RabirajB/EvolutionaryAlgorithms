#program to demonstrate particle swarm optimization algorithm
import random
import gridgraphdemo as gd
import prim_algorithm as pa
from functools import reduce
import math
import numpy as np

class Particle:
    #class used to initialize a particle
    def __init__(self, Sx, Sy, V, Xp, Yp):
        self.Sx = Sx
        self.Sy = Sy
        self.V = V
        self.Xp = Xp
        self.Yp = Yp

def particle_swarm_optimization(objgbest, p, objpbest):
    #Method for particle Swarm Optimization test
    gbest = math.ceil(1/objgbest)
    pbest = math.ceil(1/objpbest)
    Vx = p.V + 2 * random.randint(0,1) * (pbest - p.Xp) + 2 * random.randint(0, 1) * (gbest - p.Xp)
   # print(Vx)
    Vy = p.V + 2 * random.randint(0,1) * (pbest - p.Yp) + 2 * random.randint(0, 1) * (gbest - p.Yp)
   # print(Vy)
    Vnew = (Vx + Vy)//2
    
    Sxnew = p.Sx + Vx
    Synew = p.Sy + Vy
    len_S = p.Sx.size
    Xpnew = np.sum(Sxnew) // len_S
    Ypnew = np.sum(Synew) // len_S

    negatives = 0
    ratio1 = 0.9
    for i in range(len(Sxnew)):
        if Sxnew[i] < 0 or Synew[i] < 0:
            negatives = negatives + 1
    ratio2 = negatives / len(Sxnew)
    # if Xpnew < 0 or Xpnew > 500 or Ypnew < 0 or Ypnew > 500:
    if ratio2 > ratio1:
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
        
        Tx = np.append(Tx, particle.Sx[i])
        Ty = np.append(Ty, particle.Sy[i])

    distancevector = gd.get_distancevector(Tx, Ty)
    objectivefitness = pa.get_tree(distancevector)
    return objectivefitness

def particle_swarm_test(Tx, Ty):
    particles = []
    pbestvector = []
    lenTx = Tx.size
    lenTy = lenTx
    
    for i in range(150):
        len_S = lenTx - 2
        Sx = gd.get_xdata(0, 500, len_S)
        Sy = gd.get_ydata(0, 500, len_S)
        #Xs = reduce((lambda x, y: x+y), Sx) // len(Sx)
        #Ys = reduce((lambda x, y: x+y), Sy) // len(Sy)
        Xs = np.sum(Sx) // len_S
        Ys = np.sum(Sy) // len_S
        particle = Particle(Sx, Sy, 0, Xs, Ys)
        particles.append(particle)
        pbestvector.append(math.inf)
    
    for i in range(15):
        #objfitness = []

        for j in range(len(particles)):
            mst = get_fitness(Tx, Ty, particles[j])
            if mst < pbestvector[j]:
                pbestvector[j] = mst
            
            temp_len = Tx.size
            Rx = Tx[0:temp_len - lenTx]
            Ry = Ty[0:temp_len - lenTy]
            len_Rx = Rx.size
            Tx = Tx[0:temp_len - len_Rx]
            Ty = Ty[0:temp_len - len_Rx]
        best_obj_fitness = min(pbestvector)
        for j in range(len(particles)):
            particle_swarm_optimization(best_obj_fitness, particles[j], pbestvector[j])
            #print("X Coordinates of particle",particles[j].Sx)
            #print("Y Coordinates of particle",particles[j].Sy)
    particle_best = particles[pbestvector.index(min(pbestvector))]
    return particle_best


#Calling the respective modules
def call_methods(Tx,Ty,lenTx,lenTy):
    temp_len = Tx.size
    Rx = Tx[0:temp_len - lenTx]
    Ry = Ty[0:temp_len - lenTy]
    len_Rx = Rx.size
    Tx = Tx[0:temp_len - len_Rx]
    Ty = Ty[0:temp_len - len_Rx]
    #print("X coordinates =", Tx)
    #print("Y coordinates =", Ty)

    bestparticle = particle_swarm_test(Tx, Ty)
    
    temp_len = Tx.size
    Rx = Tx[0:temp_len - lenTx]
    Ry = Ty[0:temp_len - lenTy]
    len_Rx = Rx.size
    Tx = Tx[0:temp_len - len_Rx]
    Ty = Ty[0:temp_len - len_Rx]
    #print("Updated X coordinates", Tx)
    #print("Updated Y coordinates", Ty)
    '''print("X coordinates of best particle", bestparticle.Sx)
    print("Y coordinates of best particle", bestparticle.Sy)
    print("Updated X coordinates", Tx)
    print("Updated Y Coordinates", Ty)'''
    count = 0
    for i in range(len(bestparticle.Sx)):
        if bestparticle.Sx[i] < min(Tx) or bestparticle.Sx[i] > max(Tx):
            continue
        if bestparticle.Sy[i] < min(Ty) or bestparticle.Sy[i] > max(Ty):
            continue

        #Tx.append(bestparticle.Sx[i])
        #Ty.append(bestparticle.Sy[i])
        Tx = np.append(Tx, bestparticle.Sx[i])
        Ty = np.append(Ty, bestparticle.Sy[i])
        count = count + 1
    #print("Updated X Coordinates", Tx)
    #print("Updated Y Coordinates", Ty)
    distancevector = gd.get_distancevector(Tx, Ty)
    mst = pa.mst_prim(distancevector)
    mst_size = pa.get_tree(distancevector)
    #print("Size of Steiner Tree for PSO", mst_size)
    return_set = (mst_size, Tx, Ty)
    #pa.draw_gridgraph(Tx, Ty, mst,lenTx,lenTx)

    temp_len = Tx.size
    Tx = Tx[0:temp_len - count]
    Ty = Ty[0:temp_len - count]
    '''print("Restored X Coordinates=", Tx)
    print("Restored Y Coordinates=", Ty)
    print("End of PSO")'''
    return return_set
