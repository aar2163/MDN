import sys
import string
import re
import numpy as np
import json
import mdn

## Main code

##usage: centrality_atoms.py ticket centrality.csv centrality_atoms.csv enerd.npy


data = mdn.get_data(sys.argv[1])


data['output_files'] = [sys.argv[2], sys.argv[3], sys.argv[4], 'make_pdb.py']

mdn.update_data(sys.argv[1],data)


ticket = data['ticket']

f = open(sys.argv[2],'r')

#globatoms = data['topology']['global']['atoms']

out = open(sys.argv[3],'w')

saved = []

nincluded = 0

nodes = data['network']['nodes']

out.write("Atom Number,Node Betweenness,Normalized Node Betweenness\n")

for line in f:
 if(re.match(r'\d+,\d+,\d+',line)):
  l = re.split(r',',line.strip())
  name = 'Node_' + l[0]
  atoms =  mdn.dic2list(nodes[name]['atoms']) 
  for i in atoms:
   out.write("{},{},{}\n".format(i,l[1],l[2]))

out.close()
f.close()


#for i in nodes['names']:
# print nodes[i].keys()







