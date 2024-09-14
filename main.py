import numpy as np
import xml.etree.ElementTree as et
import sys

np.set_printoptions(threshold=sys.maxsize)

tree = et.parse('XML_Data/eco00220.xml')
root = tree.getroot()
for i in root.findall('entry'):
    print(i.attrib["id"], '|', str(i.attrib["name"].split(" ")[0]))
    
class MapMatrix:
    matrix_headers = []
    substances_dict = {}
    reactions_dict = {}
    
    def __init__(self, file:et) -> None:
        self.map_file = file
        self.map_root = file.getroot()
        self.map_name = root.attrib["name"]
        self.map_org = root.attrib["org"]
        self.map_number = root.attrib["number"]
        
        self.substances_dict = self.headers_init()
        
        self.matrix_headers = list(self.substances_dict.keys())
        self.matrix = np.zeros((len(self.matrix_headers), len(self.matrix_headers)))
        
        self.reactions_dict = self.reactions_init()
        
    def headers_init(self) -> dict:
        headers = {}
        for i in root.findall('entry'):
            headers[i.attrib["id"]] = str(i.attrib["name"].split(" ")[0])
        return headers
    
    def reactions_init(self) -> dict:
        reacts = {}
        self.sub_m = ''
        self.prd_m = ''
        for i in root.findall('reaction'):
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
        
        self.enders = []
        self.starters = []
        
        for i in range(len(row_zero)):
            self.enders.append(self.substances_dict[self.matrix_headers[row_zero[i]]])
        for i in range(len(col_zero)):
            self.starters.append(self.substances_dict[self.matrix_headers[col_zero[i]]])
        
        print(f"Starters: \n{self.starters}\nEnders: \n{self.enders}")
        
    def crosshair(self):
        for i in range(len(self.matrix[:,0])):
            for l in range(len(self.matrix[0,:])):
                if np.sum(self.matrix[:,0]) == np.sum(self.matrix[0,:]):
                    self.enders.append(self.substances_dict[self.matrix_headers[self.matrix[i][l]]])
                    
                       
mm = MapMatrix(tree)
print(mm.emptiness())