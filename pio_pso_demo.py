import prim_algorithm as pa
import gridgraphdemo as gd
import pigeon_optimization_algorithm as poa
import particle_swarm_optimization as pso
import constriction_factor_pso as cpso

Tx = gd.get_xdata(0, 500, 100)
Ty = gd.get_ydata(0, 500, 100)
lenx = len(Tx)
leny = len(Ty)

print("X Coordinates", Tx)
print("Y Coordinates", Ty)
distancevector = gd.get_distancevector(Tx, Ty)
mst = pa.mst_prim(distancevector)
mst_size = pa.get_tree(distancevector)
print("Size of the MST = ", mst_size)
pa.draw_gridgraph(Tx, Ty, mst)
bestp = poa.pigeon_test(Tx, Ty)
print("X coordinates =", Tx)
print("Y coordiantes =", Ty)
Tx = Tx[0:len(Tx) - len(bestp.Sx)]
Ty = Ty[0:len(Ty) - len(bestp.Sy)]
print("Updated X coordinates", Tx)
print("Updated Y coordinates", Ty)
print("X coordinates of best pigeon" , bestp.Sx)
print("Y coordinates of best pigeon" , bestp.Sy)
count = 0
for i in range(len(bestp.Sx)):
    if bestp.Sx[i] < min(Tx) or bestp.Sx[i] > max(Tx):
        continue
    if bestp.Sy[i] < min(Ty) or bestp.Sy[i] > max(Ty):
        continue

    Tx.append(bestp.Sx[i])
    Ty.append(bestp.Sy[i])
    count = count + 1
print(Tx)
print(Ty)
distancevector = gd.get_distancevector(Tx, Ty)
mst = pa.mst_prim(distancevector)
mst_size = pa.get_tree(distancevector)
print("Size of Steiner Tree for PIO", mst_size)
pa.draw_gridgraph(Tx, Ty, mst)
Tx = Tx[0: len(Tx) - count]
Ty = Ty[0: len(Ty) - count]

# Calculating for Constriction Factor PSO

bestparticle1 = cpso.constriction_factor_particle_swarm_test(Tx, Ty)
print("X coordinates =", Tx)
print("Y coordiantes =", Ty)
Tx = Tx[0:len(Tx) - len(bestparticle1.Sx)]
Ty = Ty[0:len(Ty) - len(bestparticle1.Sy)]
print("Updated X coordinates", Tx)
print("Updated Y coordinates", Ty)
print("X coordinates of best particle", bestparticle1.Sx)
print("Y coordinates of best particle", bestparticle1.Sy)
count = 0
for i in range(len(bestparticle1.Sx)):
    if bestparticle1.Sx[i] < min(Tx) or bestparticle1.Sx[i] > max(Tx):
        continue
    if bestparticle1.Sy[i] < min(Ty) or bestparticle1.Sy[i] > max(Ty):
        continue

    Tx.append(bestparticle1.Sx[i])
    Ty.append(bestparticle1.Sy[i])
    count = count + 1
print(Tx)
print(Ty)
distancevector = gd.get_distancevector(Tx, Ty)
mst = pa.mst_prim(distancevector)
mst_size = pa.get_tree(distancevector)
print("Size of Steiner Tree for Constriction Factor PSO", mst_size)
pa.draw_gridgraph(Tx, Ty, mst)
Tx = Tx[0: len(Tx) - count]
Ty = Ty[0: len(Ty) - count]

#Calculating for Normal PSO

bestparticle = pso.particle_swarm_test(Tx, Ty)
print("X coordinates =", Tx)
print("Y coordiantes =", Ty)
Tx = Tx[0:len(Tx) - len(bestp.Sx)]
Ty = Ty[0:len(Ty) - len(bestp.Sy)]
print("Updated X coordinates", Tx)
print("Updated Y coordinates", Ty)
print("X coordinates of best particle", bestparticle.Sx)
print("Y coordinates of best particle", bestparticle.Sy)
for i in range(len(bestparticle.Sx)):

    if bestparticle.Sx[i] < min(Tx) or bestparticle.Sx[i] > max(Tx):
        continue
    if bestparticle.Sy[i] < min(Ty) or bestparticle.Sy[i] > max(Ty):
        continue
    Tx.append(bestparticle.Sx[i])
    Ty.append(bestparticle.Sy[i])

distancevector = gd.get_distancevector(Tx, Ty)
mst = pa.mst_prim(distancevector)
mst_size = pa.get_tree(distancevector)
print("Size of Steiner Tree for PSO", mst_size)
pa.draw_gridgraph(Tx, Ty, mst)