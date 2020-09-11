import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import math
import random
import time as t
from pso_utils import Particle, get_fitness, particle_no, iter_no, dim, ControlInitializer

def get_velocity_position(gbest, pbest, p):
    # Method designed to find the position and the velocity attribute of the particle
    
    global particle_no
    global dim

    fitness = p.fitness / gbest.fitness
    w = 3 - math.exp(-particle_no/200) + (fitness * dim / 8)**2
    w = (1/w) + 0.8
    c = 2
    Vx = np.around((w * p.Vx) + (c * random.random() * (pbest.Sx - p.Sx)) + (c * random.random() * (gbest.Sx - p.Sx)))
    Vy = np.around((w * p.Vy) + (c * random.random() * (pbest.Sy - p.Sy)) + (c * random.random() * (gbest.Sy - p.Sy)))
    Sxnew = p.Sx + Vx
    Synew = p.Sy + Vy

    return ([Vx, Vy], Sxnew, Synew)

from pso_utils import particle_swarm_optimization, particle_swarm_test, call_methods

if __name__ == "__main__":
    # Essential parameters
    n = 10
    dim = 500
    max_iter = 25
    
    # File setup for the output
    file_name = input('Enter the file name in which you want to save the result : ')
    
    # Preprocessing on file name to check its validity
    split_name = file_name.split()
    file_name = ''
    for string in split_name:
        file_name += string.capitalize()
    if file_name == '':
        file_name = 'inertia_weighted_pso_result_'+str(dim)+'_'+str(n)
    if not '.txt' in file_name:
        file_name += '.txt'
    
    # Initializing the Controler Object that initializes the Program Controler
    control_init = ControlInitializer(n, dim, max_iter, get_velocity_position, file_name)
    
    # Controler is triggered to execute the complete program
    control_init.run()