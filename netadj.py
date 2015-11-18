import sys
import string
import re
from sets import Set
import numpy as np
import json
import mdn

"""
 Called by prepenecore.php
 Usage: python netadj.py ticket adj_fn
"""


ticket = sys.argv[1]
adj_fn = sys.argv[2]

data = mdn.get_data(ticket)

net = data['network']
nodes = net['nodes']
names = nodes['names']

top = data['topology']

nnodes = len(names)

adj = np.zeros((nnodes,nnodes)) 



for ii in range(nnodes):
 n1 = names[ii]
 """
  We want the global residue information,
  so we stored the globatom info of the first atom
  of each residue as globres in nodes.py
  globatoms format : 
  [atom_number,residue_number,molecule_name,molecule,number]
 """

 resnr1    = nodes[str(n1)]['globres'][1]
 mol_name1 = nodes[str(n1)]['globres'][2]

 bonds = top[mol_name1]['residues'][str(resnr1)]['bonds']

 adj[ii][ii] = 1 # we consider all nodes are self-bound, so this does not go into nonadj energy statistics

 for jj in range(ii+1,len(names)):
  n2 = names[jj]

  resnr2    = nodes[str(n2)]['globres'][1]
  mol_name2 = nodes[str(n2)]['globres'][2]

  if(mol_name1 != mol_name2):  ## assumption of no intermolecular bonds
   continue

  if(resnr2 in bonds):
   adj[ii][jj] = 1
   adj[jj][ii] = 1

 



np.save(adj_fn, adj)

"""
 Print some summary info
"""

print("Total nodes: {}".format(nnodes))


for name in top['mol_name']:
 try: 
  n = top[name]['netnodes']
  print("{}: {} nodes".format(name,n))
 except:
  pass

