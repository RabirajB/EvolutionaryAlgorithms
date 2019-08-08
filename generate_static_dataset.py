import gridgraphdemo as gd
import numpy as np

dim = int(input('Enter the dimension of the search space : '))
limit = int(input('Enter the limit of terminal points : '))

for i in range(10, limit+10, 10):
    Tx = gd.get_xdata(0, dim, i)
    Ty = gd.get_ydata(0, dim, i)
    filename = 'terminal_point_{0}_{1}'.format(str(dim), str(i))
    np.save(filename, np.array([Tx, Ty]))
