import prim_algorithm as pa
import gridgraphdemo as gd
import pigeon_optimization_algorithm as poa
import particle_swarm_optimization as pso
import constriction_factor_pso as cpso

Tx = gd.get_xdata(0, 500, 60)
Ty = gd.get_ydata(0, 500, 60)
#lenTx = len(Tx)
#lenTy = len(Ty)
lenTx = Tx.size
lenTy = lenTx

print("X Coordinates", Tx)
print("Y Coordinates", Ty)
distancevector = gd.get_distancevector(Tx, Ty)
mst = pa.mst_prim(distancevector)
mst_size = pa.get_tree(distancevector)
print("Size of the MST = ", mst_size)
pa.draw_gridgraph(Tx, Ty, mst,lenTx,lenTy)

poa.call_methods(Tx,Ty,lenTx,lenTy)

pso.call_methods(Tx,Ty,lenTx,lenTy)

cpso.call_methods(Tx,Ty,lenTx,lenTy)
