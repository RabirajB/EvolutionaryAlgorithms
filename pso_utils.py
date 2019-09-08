import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import math
import random
import time as t

# Global Variables
particle_no = 150
iter_no = 15
dim = 500
get_velocity_position = None

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

'''def get_velocity_position(gbest, pbest, p):
    Vx = p.V + 2 * random.randint(0,1) * (pbest - p.Xp) + 2 * random.randint(0, 1) * (gbest - p.Xp)
    Vy = p.V + 2 * random.randint(0,1) * (pbest - p.Yp) + 2 * random.randint(0, 1) * (gbest - p.Yp)
    Vnew = (Vx + Vy) // 2
    Sxnew = p.Sx + Vx
    Synew = p.Sy + Vy
    return (Vnew, Sxnew, Synew)'''

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

def particle_swarm_test(Tx, Ty, lenT):

    # Method responsible for the controlling of the whole of the PSO Algorithm
    
    particles = [] # List that stores all the particles
    global particle_no # Global Variables declared at the begening of the program
    global iter_no # Global Variables declared at the begening of the program
    len_S = lenT - 2 # Total number of Steiner points is total Terminal points - 2
    pbest = Particle(fitness=math.inf) # Initialize the Pbest particle
    gbest = Particle(fitness=math.inf) # Initialize the Gbest particle

    # Creating and initiating the Particles
    for _ in range(particle_no):
        
        Sx = gd.get_xdata(0, 500, len_S)
        Sy = gd.get_ydata(0, 500, len_S)
        
        particle = Particle(Sx, Sy, np.zeros(len_S))
        particle.fitness = get_fitness(np.copy(Tx), np.copy(Ty), particle)
        particles.append(particle)

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

# Calling the respective modules
def call_methods(Tx,Ty,lenT, func):

    # Setting the method into a method variable for dynamic linking
    global get_velocity_position
    get_velocity_position = func

    # Calling the method that controls the main optimisation algorithm
    bestparticle = particle_swarm_test(np.copy(Tx), np.copy(Ty), lenT)

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

        distancevector = gd.get_distancevector(np.copy(Tx), np.copy(Ty))
        mst_size = pa.get_tree(distancevector)

        for i in range(self.max_iter):
            print('Iteration No :', i)
            t1 = t.time()
            res = call_methods(np.copy(Tx),np.copy(Ty),lenT, self.func)
            t2 = t.time()
            data_pso[res[0]] = (res[1], res[2], t2-t1)

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