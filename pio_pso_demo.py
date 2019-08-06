import prim_algorithm as pa
import gridgraphdemo as gd
import invasive_weed_optimization as iwo
import pigeon_optimization_algorithm as poa
import particle_swarm_optimization as pso
import constriction_factor_pso as cpso
import numpy as np
import time as t

#Tx = gd.get_xdata(0, 500, 20)
#Ty = gd.get_ydata(0, 500, 20)
#lenTx = len(Tx)
#lenTy = len(Ty)
dim = 500
n = 10
Tx, Ty = np.load('terminal_point_{}_{}.npy'.format(str(dim), str(n)))
lenTx = Tx.size
lenTy = lenTx

#print("X Coordinates", Tx)
#print("Y Coordinates", Ty)
distancevector = gd.get_distancevector(Tx, Ty)
mst = pa.mst_prim(distancevector)
mst_size = pa.get_tree(distancevector)
print("Size of the MST = ", mst_size)
pa.draw_gridgraph(Tx, Ty, mst,lenTx,lenTy)

data_pio = dict()
data_pso = dict()
data_cpso = dict()

for i in range(100):
    print('Iteration No :', i)
    #print('PIO')
    t1 = t.time()
    res = poa.call_methods(Tx,Ty,lenTx,lenTy)
    t2 = t.time()
    #print('PSO')
    data_pio[res[0]] = (res[1], res[2], t2-t1)
    t2 - t.time()
    res = pso.call_methods(Tx,Ty,lenTx,lenTy)
    t3 = t.time()
    #print('CPSO')
    data_pso[res[0]] = (res[1], res[2], t3-t2)
    t3 = t.time()
    res = cpso.call_methods(Tx,Ty,lenTx,lenTy)
    t4 = t.time()
    data_cpso[res[0]] = (res[1], res[2], t4-t3)
    '''iwo.iwo_test(Tx, Ty, lenTx, lenTy)
    t5 = t.time()'''

min_pio = min(data_pio.keys())
min_pso = min(data_pso.keys())
min_cpso = min(data_cpso.keys())

print('PIO Min Wt :', min_pio)
print('X Coordinates :', data_pio[min_pio][0])
print('Y Coordinates :', data_pio[min_pio][1])
print('Time Required :', data_pio[min_pio][2])
print('Error Ratio :', min_pio/mst_size)
print('PSO Min Wt :', min_pso)
print('X Coordinates :', data_pso[min_pso][0])
print('Y Coordinates :', data_pso[min_pso][1])
print('Time Required :', data_pso[min_pso][2])
print('Error Ratio :', min_pso/mst_size)
print('CPSO Min Wt :', min_cpso)
print('X Coordinates :', data_cpso[min_cpso][0])
print('Y Coordinates :', data_cpso[min_cpso][1])
print('Time Required :', data_cpso[min_cpso][2])
print('Error Ratio :', min_cpso/mst_size)

'''print('Time Pegion Inspired Optimisation :', t2 - t1)
print('Time Particle Swarm Optimisation :', t3 - t2)
print('Time Constricted Particle Swarm Optimisation :', t4 - t3)
print('Time Invasive Weed Optimisation :', t5 - t4)'''