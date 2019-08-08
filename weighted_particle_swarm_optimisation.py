import random
import gridgraphdemo as gd
import prim_algorithm as pa
import math
import numpy as np
import random as r
from particle_swarm_optimization import Particle, get_fitness, particle_swarm_test, call_methods

def particle_swarm_optimization(objgbest, p, objpbest):
    #Method for particle Swarm Optimization test
    gbest = math.ceil(1/objgbest)
    pbest = math.ceil(1/objpbest)

    s = 150 # Number of Steiner Sets / Particles
    R = r.random() # Relative Quality
    D = 500 * 500 # Dimension of the search space

    w = 1 / (3 - np.exp(-s/200) + (R * D / 8)**2)

    Vx = w*p.V + 2 * random.randint(0,1) * (pbest - p.Xp) + 2 * random.randint(0, 1) * (gbest - p.Xp)

    Vy = w*p.V + 2 * random.randint(0,1) * (pbest - p.Yp) + 2 * random.randint(0, 1) * (gbest - p.Yp)

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
