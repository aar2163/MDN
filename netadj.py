import sys
import string
import re
from sets import Set
import numpy as np
import json
import mdn




data = mdn.get_data(sys.argv[1])

net = data['network']
nodes = net['nodes']
names = nodes['names']

top = data['topology']

nnodes = len(names)

bonded = np.zeros((nnodes,nnodes)) ## chemical bonds, (ii,jj) is 1 if pair is bound, 0 otherwise


#print net['nodes']['Node_0']


for ii in range(len(names)):
 n1 = names[ii]
 mol_name1 = nodes[str(n1)]['globres'][2]
 resnr1 = nodes[str(n1)]['globres'][1]
 bonds = top[mol_name1]['residues'][str(resnr1)]['bonds']

 bonded[ii][ii] = 1 # we consider all nodes are self-bound, so this does not go into nonbonded energy statistics

 for jj in range(ii+1,len(names)):
  n2 = names[jj]
  mol_name2 = nodes[str(n2)]['globres'][2]

  if(mol_name1 != mol_name2):  ## assumption of no intermolecular bonds
   continue
  resnr2 = nodes[str(n2)]['globres'][1]
  if(resnr2 in bonds):
   bonded[ii][jj] = 1
   bonded[jj][ii] = 1

 



np.save(sys.argv[2],bonded)

print("Total nodes: {}".format(nnodes))


for name in top['mol_name']:
 try: 
  n = top[name]['netnodes']
  print("{}: {} nodes".format(name,n))
 except:
  pass

