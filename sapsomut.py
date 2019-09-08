import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import math
import random
import time as t
from pso_utils import Particle, get_fitness, particle_no, iter_no, dim

current_iter = 1

def get_velocity_position(gbest, pbest, p):
    # Method designed to find the position and the velocity attribute of the particle
    
    global particle_no
    global dim
    global current_iter
    
    fitness = p.fitness / gbest.fitness
    w = 3 - math.exp(-particle_no/200) + (fitness * dim / 8)**2
    w = (1/w) + 0.8
    c = 2 - ((0.5/iter_no) * current_iter)
    Vx = np.around((w * p.Vx) + (c * random.random() * (pbest.Sx - p.Sx)) + (c * random.random() * (gbest.Sx - p.Sx)))
    Vy = np.around((w * p.Vy) + (c * random.random() * (pbest.Sy - p.Sy)) + (c * random.random() * (gbest.Sy - p.Sy)))
    Sxnew = np.around((c * random.random() * p.Sx) + Vx)
    Synew = np.around((c * random.random() * p.Sy) + Vy)
    current_iter += 1
    
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