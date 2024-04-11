import math
from timeit import default_timer
from heapdict import heapdict

class Graph:
    def __init__(self):
        self.adjList = {}

    def addEdge(self, source, destination, weight):
        if source in self.adjList:
            self.adjList[source].append((source, destination, weight))
        else:
            self.adjList[source] = [(source, destination, weight)]

        if destination in self.adjList:
            self.adjList[destination].append((destination, source, weight))
        else:
            self.adjList[destination] = [(destination, source, weight)]

    def dijkstra(self, source):
        pq = heapdict()
        weights = {}
        parents = {}
        dq = set()
        
        for v in self.adjList:
            if v == source:
                pq[v] = 0
            else:
                pq[v] = math.inf
          
        weights[source] = 0
        parents[source] = None

        while len(pq) > 0:
            current, weight = pq.popitem()
            dq.add(current)
            weights[current] = weight
            
            for adjEdge in self.adjList[current]:
                adj = adjEdge[1] if adjEdge[0] == current else adjEdge[0]

                if adj in dq:
                    continue
                
                calcWeight = weights[current] + adjEdge[2]
                adjWeight = pq.get(adj)

                if calcWeight < adjWeight:
                    pq[adj] = calcWeight
                    parents[adj] = current

        self.outerParents = parents
        return weights

    def findShortestPathHelper(self, vertex, parents, path):
        if vertex == None or not vertex in parents:
            return []
        return self.findShortestPathHelper(parents[vertex], parents, path) + [(vertex, path[vertex])]
    
    def findShortestPath(self, source, destination):
        start_time = default_timer()
        path = self.dijkstra(source)
        shortestPath = self.findShortestPathHelper(destination, self.outerParents, path)
        return (tuple(map(lambda a: a[0], shortestPath)), shortestPath[-1][1], default_timer() - start_time)