import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import time as t
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Global Variables
gpso_max_iter = 50 # Defines the maximum iteration of the GPSO algorithm
grad_max_iter = 5 # Defines the number of gradient descent cycles
iter_no = 3 # Imported from pso_utils. Defines the number of PSO iteration cycles
px_vect = []
py_vect = []
cost_vect = []
particle_no = 150
dim = 500
get_velocity_position = None
particles = [] # List that stores all the particles


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

class Particle:
    # Class used to initialize a particle
    def __init__(self, Sx=0, Sy=0, V=[0, 0], fitness = None):
        self.Sx = Sx
        self.Sy = Sy
        self.Vx = V[0]
        self.Vy = V[1]
        self.fitness = fitness

def get_fitness(Tx, Ty, particle):
    # Method to find the Objective Fitness (MST Weight)

    # Setting the checking boundaries
    maxTx = np.amax(Tx)
    minTx = np.amin(Tx)
    maxTy = np.amax(Ty)
    minTy = np.amin(Ty)

    # Constructing the coordinate set of the Tree with Steiner Points
    for i in range(particle.Sx.size):
        if particle.Sx[i] < minTx or particle.Sx[i] > maxTx:
            continue
        if particle.Sy[i] < minTy or particle.Sy[i] > maxTy:
            continue
        
        Tx = np.append(Tx, particle.Sx[i])
        Ty = np.append(Ty, particle.Sy[i])

    # Finding the Objective Fitness
    distancevector = gd.get_distancevector(Tx, Ty)
    objectivefitness = pa.get_tree(distancevector)
    return objectivefitness

def particle_swarm_optimization(Tx, Ty, gbest, p, pbest):
    
    # Method for particle Swarm Optimization test

    Vnew, Sxnew, Synew = get_velocity_position(gbest, pbest, p)

    len_S = p.Sx.size

    negatives = 0
    ratio1 = 0.9
    for i in range(len_S):
        if Sxnew[i] < 0 or Synew[i] < 0:
            negatives = negatives + 1
    ratio2 = negatives / len_S

    if ratio2 > ratio1:
        pass

    else:
        p.Sx = Sxnew
        p.Sy = Synew
        p.Vx = Vnew[0]
        p.Vy = Vnew[1]
        p.fitness = get_fitness(np.copy(Tx), np.copy(Ty), p)

def create_particles(Tx, Ty, len_S):

    # Method to create the swarm of Particles object

    global particle_no # Global Variables declared at the begening of the program
    global particles

    particles = []
    # Creating and initiating the Particles
    for _ in range(particle_no):
        
        Sx = gd.get_xdata(0, 500, len_S)
        Sy = gd.get_ydata(0, 500, len_S)
        
        particle = Particle(Sx, Sy)
        particle.fitness = get_fitness(np.copy(Tx), np.copy(Ty), particle)
        particles.append(particle)
    

def particle_swarm_test(Tx, Ty, lenT):

    # Method responsible for the controlling of the whole of the PSO Algorithm
    
    global iter_no # Global Variables declared at the begening of the program
    pbest = Particle(fitness=math.inf) # Initialize the Pbest particle
    gbest = Particle(fitness=math.inf) # Initialize the Gbest particle

    # Running the PSO
    for _ in range(iter_no):

        # Finding the Pbest
        for j in range(particle_no):
            mst = particles[j].fitness
            if mst < pbest.fitness:
                pbest.Sx = np.copy(particles[j].Sx)
                pbest.Sy = np.copy(particles[j].Sy)
                pbest.Vx = np.copy(particles[j].Vx)
                pbest.Vy = np.copy(particles[j].Vy)
                pbest.fitness = mst
        
        # Finding the Gbest
        if gbest.fitness > pbest.fitness:
            gbest.Sx = np.copy(pbest.Sx)
            gbest.Sy = np.copy(pbest.Sy)
            gbest.Vx = np.copy(pbest.Vx)
            gbest.Vy = np.copy(pbest.Vy)
            gbest.fitness = pbest.fitness
        
        for j in range(particle_no):
            # Calling the Optimization Algorithm
            particle_swarm_optimization(Tx, Ty, gbest, particles[j], pbest)
           
    return gbest

def call_methods(Tx,Ty,lenT, func):
    
    # Performance controler of the PSO
    
    global cost_vect
    global px_vect
    global py_vect
    
    # Setting the method into a method variable for dynamic linking
    global get_velocity_position
    get_velocity_position = func

    bestparticle = Particle(fitness=math.inf)

    # Running the GPSO Iterations
    for i in range(gpso_max_iter):
        # Running PSO algorithm
        bestparticle_local = particle_swarm_test(np.copy(Tx), np.copy(Ty), lenT)

        if bestparticle_local.fitness < bestparticle.fitness:
            bestparticle = bestparticle_local

        # Running Gradient Cycles
        px = np.mean(bestparticle_local.Sx)
        py = np.mean(bestparticle_local.Sy)

        for _ in range(grad_max_iter):
            
            cost = search_function(px, py)
            cost_vect.append(cost)
            px_vect.append(px)
            py_vect.append(py)
            grad = gradient(px, py)
            px, py = update_params(px, py, grad[0], grad[1])

        new_Sx = bestparticle_local.Sx + round(px)
        new_Sy = bestparticle_local.Sy + round(py)

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
    return_set = (mst_size, Tx, Ty, mst)

    return return_set

def plot_results():
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(np.array(px_vect), np.array(py_vect), np.array(cost_vect))
    ax = fig.add_subplot(112, projection='3d')
    ax.plot3D(np.array(px_vect), np.array(py_vect), np.array(cost_vect))
    ax = fig.add_subplot(211, projection='3d')
    ax.plot_wireframe(np.array(px_vect), np.array(py_vect), np.array(cost_vect))


class ControlInitializer:
    def __init__(self, n, dim, max_iter, func, file_name):
        self.n = n
        self.dim = dim
        self.max_iter = max_iter
        self.func = func
        self.file_name = file_name

        

    def run(self):

        Tx, Ty = np.load('terminal_point_{}_{}.npy'.format(str(self.dim), str(self.n)))
        lenT = Tx.size
        data_pso = dict()
        len_S = lenT - 2 # Total number of Steiner points is total Terminal points - 2

        distancevector = gd.get_distancevector(np.copy(Tx), np.copy(Ty))
        mst_size = pa.get_tree(distancevector)

        for i in range(self.max_iter):
            print('Iteration No :', i)
            
            # Creating and initiating the Particles
            create_particles(Tx, Ty, len_S)
            
            t1 = t.time()
            res = call_methods(np.copy(Tx),np.copy(Ty),lenT, self.func)
            t2 = t.time()
            data_pso[res[0]] = (res[1], res[2], t2-t1, res[3])

        min_pso = min(data_pso.keys())

        fp = open(self.file_name, 'w')
        fp.write("Size of the MST = " + str(mst_size) + '\n')
        fp.write('No. of Iterations :' + str(self.max_iter) + '\n')
        fp.write('PSO Min Wt :'+ str(min_pso) + '\n')
        fp.write('X Coordinates :'+ str(data_pso[min_pso][0]) + '\n')
        fp.write('Y Coordinates :'+ str(data_pso[min_pso][1]) + '\n')
        fp.write('No. of Steiner points :'+ str(data_pso[min_pso][0].size - self.n) + '\n')
        fp.write('Time Required :'+ str(data_pso[min_pso][2]) + '\n')
        fp.write('Error Ratio :'+ str(min_pso/mst_size) + '\n')
        fp.close()

        # Ploting the RSMT
        pa.draw_gridgraph(Tx, Ty, data_pso[min_pso][3], lenT, lenT)
        #plot_results()