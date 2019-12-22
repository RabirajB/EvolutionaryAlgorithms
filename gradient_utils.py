import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import time as t

from pso_utils import particle_no, dim, get_velocity_position

gpso_max_iter = 50 # Defines the maximum iteration of the GPSO algorithm
grad_max_iter = 5 # Defines the number of gradient descent cycles
iter_no = 3 # Imported from pso_utils. Defines the number of PSO iteration cycles
px_vect = []
py_vect = []
cost_vect = []

from pso_utils import Particle, ControlInitializer
from pso_utils import get_fitness, particle_swarm_optimization, particle_swarm_test

'''def get_cost(fitness, px, py, gbest_x, gbest_y, n, b=0.3):
    cost_x = fitness * np.sum((px/2)**2 - (gbest_x + b)*px) / n
    cost_y = fitness * np.sum((py/2)**2 - (gbest_y + b)*py) / n
    return (cost_x, cost_y)

def gradient(fitness, px, py, gbest_x, gbest_y, n, b=0.3):
    grad_x = fitness * np.sum(px - gbest_x + b) / n
    grad_y = fitness * np.sum(py - gbest_y + b) / n
    return (grad_x, grad_y)

def update_params(px, py, grad_x, grad_y, alpha=0.32):
    px_new = px - alpha*grad_x
    py_new = py - alpha*grad_y
    return (px_new, py_new)'''

def search_function(x1, x2):
    # This method returns the value evaluated by the predefined local search function
    
    return x1**2 - (2 * x1 * x2) + (4 * x2**2) # Local Search function

def gradient(x1, x2):
    # Method returns the evaluation of the gradient of the local search function

    dx1 = 2*x1 - 2*x2
    dx2 = -2*x1 + (8 * x2)
    return (dx1, dx2)

def update_params(px, py, dx1, dx2, alpha=0.32):
    # Performs the update parameter operation of the gradient descent
    
    px -= alpha*dx1
    py -= alpha*dx2
    return (px, py)

def call_methods(Tx,Ty,lenT, func):

    # Setting the method into a method variable for dynamic linking
    global get_velocity_position
    get_velocity_position = func

    # Running the GPSO Iterations
    for i in range(gpso_max_iter):
        # Calling the method that controls the main optimisation algorithm
        if i == 0:
            bestparticle = particle_swarm_test(np.copy(Tx), np.copy(Ty), lenT)
        else:
            bestparticle = particle_swarm_test(np.copy(Tx), np.copy(Ty), lenT, False)

        # Running Gradient Cycles
        px = np.mean(bestparticle.Sx)
        py = np.mean(bestparticle.Sy)

        for _ in range(grad_max_iter):
            
            cost = search_function(px, py)
            cost_vect.append(cost)
            px_vect.append(px)
            py_vect.append(py)
            grad = gradient(px, py)
            px, py = update_params(px, py, grad[0], grad[1])

        new_Sx = bestparticle.Sx + round(px)
        new_Sy = bestparticle.Sy + round(py)

        new_fitness = get_fitness(np.copy(Tx), np.copy(Ty), Particle(new_Sx, new_Sy))
        if new_fitness < bestparticle.fitness:
            bestparticle.fitness = new_fitness
            bestparticle.Sx = new_Sx
            bestparticle.Sy = new_Sy

    # Extracting the position of the Steiner Points from the best particle
    for i in range(bestparticle.Sx.size):
        if bestparticle.Sx[i] < min(Tx) or bestparticle.Sx[i] > max(Tx):
            continue
        if bestparticle.Sy[i] < min(Ty) or bestparticle.Sy[i] > max(Ty):
            continue

        Tx = np.append(Tx, bestparticle.Sx[i])
        Ty = np.append(Ty, bestparticle.Sy[i])

    # Finding the MST of the final RSMT
    distancevector = gd.get_distancevector(Tx, Ty)
    mst = pa.mst_prim(distancevector)
    mst_size = pa.get_tree(distancevector)

    # Building the final return tuple for the use in the main program
    return_set = (mst_size, Tx, Ty)

    # Ploting the RSMT
    pa.draw_gridgraph(Tx, Ty, mst,lenT,lenT)

    return return_set