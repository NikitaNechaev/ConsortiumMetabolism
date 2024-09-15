import numpy as np
import xml.etree.ElementTree as et
import sys
import os
from tqdm import tqdm
from pyvis.network import Network
import random
import pandas as pd

np.set_printoptions(threshold=sys.maxsize)
    
class MapMatrix:
    matrix_headers = []
    substances_dict = {}
    reactions_dict = {}
    
    def __init__(self, file:et) -> None:
        self.map_file = file
        self.map_root = file.getroot()
        self.map_name = self.map_root.attrib["name"]
        self.map_org = self.map_root.attrib["org"]
        self.map_number = self.map_root.attrib["number"]
        
        self.substances_dict = self.headers_init()
        
        self.matrix_headers = list(self.substances_dict.keys())
        self.matrix = np.zeros((len(self.matrix_headers), len(self.matrix_headers)))
        
        self.reactions_dict = self.reactions_init()
        
        self.enders = []
        self.starters = []
        self.emptiness()
        
    def headers_init(self) -> dict:
        headers = {}
        for i in self.map_root.findall('entry'):
            headers[i.attrib["id"]] = str(i.attrib["name"].split(" ")[0])
        return headers
    
    def reactions_init(self) -> dict:
        reacts = {}
        self.sub_m = ''
        self.prd_m = ''
        for i in self.map_root.findall('reaction'):
            self.sub_m = self.matrix_headers.index(str(i.find("substrate").attrib["id"]))
            self.prd_m = self.matrix_headers.index(str(i.find("product").attrib["id"]))
            self.matrix[self.sub_m, self.prd_m] = i.attrib["id"]
            reacts[i.attrib["id"]] = i.attrib["name"]
        return reacts
    
    def emptiness (self):
        rows = np.sum(self.matrix, axis=1)
        cols = np.sum(self.matrix, axis=0)
        row_zero = []
        col_zero = []
        
        for i in range(len(rows)):
            if rows[i] == 0 and cols[i] != 0:
                row_zero.append(i)
        for l in range(len(cols)):
            if cols[l] == 0 and rows[l] != 0:
                col_zero.append(l)
        
        for i in range(len(row_zero)):
            self.enders.append(self.substances_dict[self.matrix_headers[row_zero[i]]])
        for i in range(len(col_zero)):
            self.starters.append(self.substances_dict[self.matrix_headers[col_zero[i]]])
        
        self.crosshair()  

        #print(f"Starters: \n{self.starters}\nEnders: \n{self.enders}")
        
    def crosshair(self):
        for i in range(len(self.matrix[:,0])):
            for l in range(len(self.matrix[0,:])):
                if np.sum(self.matrix[:,0]) == np.sum(self.matrix[0,:]) and np.sum(self.matrix[:,0]) != 0:
                    self.enders.append(self.substances_dict[self.matrix_headers.index(int(self.matrix[i][l]))])


maps = []
for i in tqdm(os.listdir("XML_Data")):
    tree = et.parse(f'XML_Data/{i}')
    maps.append(MapMatrix(tree))
    
full_dict = {}

f = open('out.txt', 'w')
out_graph = []

for i in maps:
    full_dict[i.map_name] = {"starters": i.starters, "enders": i.enders}
for i in tqdm(maps):
    for l in maps:
        for j in range(len(full_dict[i.map_name]["starters"])):
            if full_dict[i.map_name]["starters"][j] in full_dict[l.map_name]["enders"]:
                f.write(f"{i.map_name}, {l.map_name}, {full_dict[i.map_name]["starters"][j]}\n")
                out_graph.append([i.map_name, l.map_name, full_dict[i.map_name]["starters"][j]])               

net = Network(height='1000px', width='100%')

node_ids = []
node_labels = []
node_colors = []
node_weights = []
edges = []

#net.barnes_hut()

r = lambda: random.randint(0,255)
print('#%02X%02X%02X' % (r(),r(),r()))

for i in maps:
    node_ids.append(i.map_name)
    node_labels.append(i.map_org)
    node_weights.append(out_graph[0].count(i.map_name) + out_graph[1].count(i.map_name))
    r = lambda: random.randint(0,255)
    node_colors.append('#%02X%02X%02X' % (r(),r(),r()))
for i in range(len(out_graph)):
    edges.append((out_graph[i][0], out_graph[i][1]))

net.add_nodes(node_ids, color = node_colors, value = node_weights)
net.add_edges(edges)
net.toggle_physics(False)
net.show('graph.html', notebook=False)