import math
import gridgraphdemo as gd
import matplotlib.pyplot as plot


class Min_Item:
    def __init__(self, minitem,  item_id):
        self.minitem = minitem
        self.item_id = item_id

class Vertex:
    #Class containing the definition of a vertex including key, parent , vertex_id
    def __init__(self,key,parent,vertex_id):
        self.key = key
        self.parent = parent
        self.vertex_id = vertex_id

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def insert(self, vertex):
        self.queue.append(vertex)

    def is_empty(self):
        return self.queue == []

    def check_presence(self, vertex):
        for i in self.queue:
            if vertex.vertex_id == i.vertex_id:
                return True
        return False

    def show_vertices(self):
        for i in range(len(self.queue)):
            print(self.queue[i].vertex_id)

    def extract_min(self):
        min = 0
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].key < self.queue[min].key:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()

def get_min_item(arr,row_id):
    min = math.inf
    index = 0
    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i]
            index = i
    item = Min_Item(min, index)
    return item

def mst_prim(distancevector):

    priorityqueue = PriorityQueue()
    keys = []
    mst = []
    for i in range(len(distancevector)):
        v = Vertex(math.inf, None, i)
        keys.append(v)
    keys[0].key = 0
    start = keys[0]
    priorityqueue.insert(start)
    #priorityqueue.show_vertices()
    mst.append(start)
    while priorityqueue.is_empty() is not True:
        u = priorityqueue.extract_min()
        index = u.vertex_id
        if u not in mst:
            mst.append(u)
        for i in range(len(distancevector[index])):
            v = keys[i]
            if v not in mst and distancevector[index][i] < v.key:
                v.parent = u
                v.key = distancevector[index][i]
                priorityqueue.insert(v)
                keys[i] = v

    return mst

def get_tree(distancevector):
    mst = mst_prim(distancevector)
    #print("Printing")
    i = 1
    mst_size = 0
    while i < len(mst):
        u = mst[i].parent
        #print(u.vertex_id, "->", mst[i].vertex_id)
        mst_size += mst[i].key
        i = i+1

    return mst_size

def draw_gridgraph(Tx,Ty,mst,lenTx,lenTy):
    i = 1
    while i in range(len(mst)):
        u = mst[i].parent
        Sx = Tx[u.vertex_id]
        Sy = Ty[u.vertex_id]
        destx = Tx[mst[i].vertex_id]
        desty = Ty[mst[i].vertex_id]
        gd.figure_plot(Sx, Sy, destx, desty, u.vertex_id, mst[i].vertex_id,lenTx,lenTy)
        i = i+1
    plot.show()






















