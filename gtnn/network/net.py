import graph_tool.all as gt
import numpy as np


class Net(object):
    __valueType = "long double"
    biasProp = None
    valueProp = None
    weightProp = None

    def __init__(self,  nInput=1, nOutput=1, graph=gt.Graph()):
        self.g = gt.Graph(graph)
        self.__nInput = nInput
        self.__nOutput = nOutput
        self.properties = dict()
        #TODO: przerzuc do slownika property
        self.biasProp = self.g.new_vertex_property(Net.__valueType)
        self.valueProp = self.g.new_vertex_property(Net.__valueType)
        self.weightProp = self.g.new_edge_property(Net.__valueType)
        self.activation = self.g.new_vertex_property("python::object")
        self.prepare()

    def addVertexProperty(self, name, typeName):
        self.properties[name] = self.g.new_vertex_property(typeName)
        return self.properties[name]

    def addEdgeProperty(self, name, typeName):
        self.properties[name] = self.g.new_edge_property(typeName)
        return self.properties[name]

    def prepare(self):
        """
        Computes ans saves the topological sort of the graph for future use.
        """
        self.order = np.array(gt.topological_sort(self.g)[::-1])

    def forward(self, inputVals=[]):
        g = self.g
        vp = self.valueProp
        bp = self.biasProp
        wp = self.weightProp

        for inpVal, vIdx in zip(inputVals, self.order):
            vp[g.vertex(vIdx)] = inpVal

        for vIdx in self.order[self.__nInput:]:
            v = g.vertex(vIdx)

            inputs = np.array([vp[e.source()] for e in v.in_edges()])
            weights = np.array([wp[e] for e in v.in_edges()])

            vp[v] = np.sum(inputs * weights) + bp[v]
            

        return np.array(vp.a[-self.__nOutput:])