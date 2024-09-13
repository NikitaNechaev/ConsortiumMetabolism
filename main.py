from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import xml.etree.ElementTree as et

tree = et.parse('XML_Data/eco00220.xml')
root = tree.getroot()
print(type(tree))
for i in root.findall('entry'):
    print(i.attrib["id"], '|', str(i.attrib["name"].split(" ")[0]))
    
class MapMatrix: 
    def __init__(self, file:et) -> None:
        self.map_file = file
        self.map_root = file.getroot()
        self.map_name = root.attrib["name"]
        self.map_org = root.attrib["org"]
        self.map_number = root.attrib["number"]
        
        self.substances_dict = self.headers_init(self.map_file)
        self.reactions_dict = {}
        
        self.matrix_headers = list(self.substances_dict.keys())
        self.matrix = np.zeros((len(self.matrix_headers), len(self.matrix_headers)))
        
    def headers_init(self, file: et) -> dict:
        headers = {}
        for i in root.findall('entry'):
            headers[i.attrib["id"]] = str(i.attrib["name"].split(" ")[0])
        return headers
            
               

mm = MapMatrix(tree)
print(mm.map_name, mm.map_org, mm.map_number)