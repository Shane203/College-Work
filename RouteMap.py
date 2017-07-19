#Shane Houston (115477508)
from APQ import Element, APQ

class Vertex:
    """ A Vertex in a graph. """
    
    def __init__(self, element, lat, long):
        """ Create a vertex, with data element. """
        self._element = element
        self._lat = lat
        self._long = long

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element
    
class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """
    
    def __init__(self, v, w, element):
        """ Create an edge between vertice v and w, with label element.

            element can be an arbitrarily complex structure.
        """
        self._vertices = (v,w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                   + str(self._vertices[1]) + ' : '
                   + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered. pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge. """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element

class RouteMap(object):
    def __init__(self):
        self._structure = dict()
        self._reverse = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        if self.num_vertices() < 100 and self.num_edges() < 100:
            hstr = ('|V| = ' + str(self.num_vertices())
                    + '; |E| = ' + str(self.num_edges()))
            vstr = '\nVertices: '
            for v in self._structure:
                vstr += str(v) + '-'
            edges = self.edges()
            estr = '\nEdges: '
            for e in edges:
                estr += str(e) + ' '
            return hstr + vstr + estr
        return "String too large to print"

    #--------------------------------------------------#
    #ADT methods to query the graph
    
    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])    #the dict of edges for v
        return num //2     #divide by 2, since each edege appears in the
                           #vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ get the first vertex that matches element. """
        return self._reverse[element]

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                #to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v. """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None. """
        if (self._structure != None
                         and v in self._structure
                         and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def get_in_edges(self,v):
        """ Return a list of all in edges incident on v. """
        edges = []
        for e in self.get_edges(v):
            if e.end() == v:
                edges.append(e)
        return edges

    def get_out_edges(self,v):
        """ Return a list of all out edges incident on v. """
        edges = []
        for e in self.get_edges(v):
            if e.start() == v:
                edges.append(e)
        return edges

    def in_degree(self, v):
        """ Return the in degree of vertex v. """
        return len(self.get_in_edges(v))

    def out_degree(self, v):
        """ Return the out degree of vertex v. """
        return len(self.get_out_edges(v))

    def degree(self, v):
        """ Return the degree of vertex v. """
        return len(self._structure[v])

    #--------------------------------------------------#
    #ADT methods to modify the graph
    
    def add_vertex(self, element, lat, long):
        """ Add a new vertex with data element.

            If there is already a vertex with the same data element,
            this will create another vertex instance.
        """
        v = Vertex(element, lat, long)
        self._structure[v] = dict()
        self._reverse[element] = v
        return v

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

            If either v or w are not vertices in the graph, does not add, and
            returns None.
            
            If an edge already exists between v and w, this will
            replace the previous edge.
        """
        if not v in self._structure or not w in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements. """
        for (v,w) in elist:
            self.add_edge(v,w,None)

    #-----------------------------------------#

    def sp(self,v,w):
        closed = self.dijkstra(v)
        cost, pred_elt = closed[w]
        pred = self.get_vertex_by_label(pred_elt)
        path = []
        path.append([w, cost])
        while closed[pred][1] is not None :
            path.append([pred, closed[pred][0]])
            pred = self.get_vertex_by_label(closed[pred][1])
        path.append([v, 0])
        return path

    def printvlist(self,path):
        print("%-10s, %-10s, %-10s, %-10s, %-10s" % \
              ("type","latitude","longitude","element","cost"))
        for pair in reversed(path):
            print("%-10s, %-10s, %-10s, %-10s, %-10s" % \
                  ("w", pair[0]._lat, pair[0]._long, pair[0]._element, pair[1]))
    
    def dijkstra(self, s):
        open = APQ()
        locs = dict()
        closed = dict()
        preds = dict()
        preds[s]=None

        start = open.add(0, s)
        locs[s] = start
        while not open.is_empty():
            v = open.remove_min()
            cost = v.key
            elt = v.value
            try:
                del locs[elt]
            except KeyError:
                pass
            pre = preds.pop(elt)
            if pre is None:
                closed[elt] = [cost, pre]
            else:
                closed[elt] = [cost, pre.element()]
            for e in self.get_edges(elt):
                w = e.opposite(elt)
                if w not in closed:
                    newcost = cost + e.element()
                    if w not in locs:
                        preds[w] = elt
                        new = open.add(newcost, w)
                        locs[w] = new
                    elif newcost < locs[w].key:
                        preds[w] = elt
                        open.update_key(locs[w], newcost)
        return closed

    #-----------------------------------#

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = RouteMap()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        gps = file.readline().split()[1:]
        vertex = graph.add_vertex(nodeid, gps[0], gps[1])
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = file.readline() # Skipping length
        time = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, time)
        oneway = file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph


routemap = graphreader('corkCityData.txt')
ids = {}
ids['wgb'] = 1669466540
ids['turnerscross'] = 348809726
ids['neptune'] = 1147697924
ids['cuh'] = 860206013
ids['oldoak'] = 358357
ids['gaol'] = 3777201945
ids['mahonpoint'] = 330068634
sourcestr = 'wgb'
deststr='mahonpoint'
source = routemap.get_vertex_by_label(ids[sourcestr])
dest = routemap.get_vertex_by_label(ids[deststr])
tree = routemap.sp(source,dest)
routemap.printvlist(tree)
    
