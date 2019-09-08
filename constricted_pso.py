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
    if not '.txt' in file_name:
        file_name += '.txt'
    
    # Initializing the Controler Object that initializes the Program Controler
    control_init = ControlInitializer(n, dim, max_iter, get_velocity_position, file_name)
    
    # Controler is triggered to execute the complete program
    control_init.run()