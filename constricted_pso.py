import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import math
import random
import time as t
from pso_utils import Particle, get_fitness, particle_no, iter_no, dim

def get_velocity_position(gbest, pbest, p):
    # Method designed to find the position and the velocity attribute of the particle
    
    global particle_no
    global dim

    c1 = 2
    c2 = 2

    phi1 = c1 * random.random()
    phi2 = c2 * random.random()
    phi_res = phi1 + phi2
    X = 2 / (2 - phi_res - math.sqrt(phi_res**2 - (4 * phi_res)))

    Vx = np.around(X * (p.Vx + (phi1 * (pbest.Sx - p.Sx)) + phi2 * (gbest.Sx - p.Sx)))
    Vy = np.around(X * (p.Vy + (phi1 * (pbest.Sy - p.Sy)) + phi2 * (gbest.Sy - p.Sy)))
    Sxnew = p.Sx + Vx
    Synew = p.Sy + Vy

    return ([Vx, Vy], Sxnew, Synew)

from pso_utils import particle_swarm_optimization, particle_swarm_test, call_methods

if __name__ == "__main__":
    n = 10
    Tx, Ty = np.load('terminal_point_{}_{}.npy'.format(str(dim), str(n)))
    lenT = Tx.size
    max_iter = 25
    data_pso = dict()

    distancevector = gd.get_distancevector(np.copy(Tx), np.copy(Ty))
    mst = pa.mst_prim(distancevector)
    mst_size = pa.get_tree(distancevector)

    for i in range(max_iter):
        print('Iteration No :', i)
        t1 = t.time()
        res = call_methods(np.copy(Tx),np.copy(Ty),lenT, get_velocity_position)
        t2 = t.time()
        data_pso[res[0]] = (res[1], res[2], t2-t1)

    min_pso = min(data_pso.keys())

    fp = open('result_sapsomut.txt', 'w')
    fp.write("Size of the MST = " + str(mst_size) + '\n')
    fp.write('No. of Iterations :' + str(max_iter) + '\n')
    fp.write('PSO Min Wt :'+ str(min_pso) + '\n')
    fp.write('X Coordinates :'+ str(data_pso[min_pso][0]) + '\n')
    fp.write('Y Coordinates :'+ str(data_pso[min_pso][1]) + '\n')
    fp.write('No. of Steiner points :'+ str(data_pso[min_pso][0].size - n) + '\n')
    fp.write('Time Required :'+ str(data_pso[min_pso][2]) + '\n')
    fp.write('Error Ratio :'+ str(min_pso/mst_size) + '\n')
    fp.close()