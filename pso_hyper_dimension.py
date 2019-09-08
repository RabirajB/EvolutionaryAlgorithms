import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import math
import random
import time as t
from pso_utils import Particle, get_fitness, particle_no, iter_no, dim, ControlInitializer


def get_velocity_position(gbest, pbest, p):
    # Method designed to find the position and the velocity attribute of the particle

    Vx = np.around(p.Vx + 2 * random.random() * (pbest.Sx - p.Sx) + 2 * random.random() * (gbest.Sx - p.Sx))
    Vy = np.around(p.Vy + 2 * random.random() * (pbest.Sy - p.Sy) + 2 * random.random() * (gbest.Sy - p.Sy))
    Sxnew = p.Sx + Vx
    Synew = p.Sy + Vy
    return ([Vx, Vy], Sxnew, Synew)

from pso_utils import particle_swarm_optimization, particle_swarm_test, call_methods


if __name__ == "__main__":
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
