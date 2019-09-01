import numpy as np
import gridgraphdemo as gd
import prim_algorithm as pa
import math
import random

class Particle:
    #class used to initialize a particle
    def __init__(self, Sx=0, Sy=0, V=0, fitness = None):
        self.Sx = Sx
        self.Sy = Sy
        self.V = V
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
    
    #Method for particle Swarm Optimization test

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
        p.V = Vnew
        p.fitness = get_fitness(np.copy(Tx), np.copy(Ty), p)

def particle_swarm_test(Tx, Ty, lenT):

    # Method responsible for the controlling of the whole of the PSO Algorithm
    
    particles = []
    particle_no = 150
    len_S = lenT - 2  # Total number of Steiner points is total Terminal points - 2
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
    for _ in range(15):

        # Finding the Pbest
        for j in range(particle_no):
            mst = particles[j].fitness
            if mst < pbest.fitness:
                pbest.Sx = np.copy(particles[j].Sx)
                pbest.Sy = np.copy(particles[j].Sy)
                pbest.V = np.copy(particles[j].V)
                pbest.fitness = mst
        
        # Finding the Gbest
        if gbest.fitness > pbest.fitness:
            gbest.Sx = np.copy(pbest.Sx)
            gbest.Sy = np.copy(pbest.Sy)
            gbest.V = np.copy(pbest.V)
            gbest.fitness = pbest.fitness
        
        for j in range(particle_no):
            # Calling the Optimization Algorithm
            particle_swarm_optimization(Tx, Ty, gbest, particles[j], pbest)
           
    return gbest

# Calling the respective modules
def call_methods(Tx,Ty,lenTx,lenTy):

    # Calling the method that controls the main optimisation algorithm
    bestparticle = particle_swarm_test(np.copy(Tx), np.copy(Ty), lenTx)

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
    pa.draw_gridgraph(Tx, Ty, mst,lenTx,lenTx)

    return return_set