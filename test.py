import numpy as np
import xml.etree.ElementTree as et

tree = et.parse('XML_Data/eco00220.xml')
root = tree.getroot()

a = np.array([[1,2,3],
              [4,5,6],
              [7,8,9]])
print(a)
sum = np.sum(a , axis=0)
# 1 - row
# 0 - 
print(sum)