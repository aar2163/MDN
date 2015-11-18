import sys
import string
import re
from sets import Set
import numpy as np
import json
import mdn

"""
 Creates a matrix indicating which pathways
 should be calculated

 Called by analysis.php
 Usage: python ticket fname g1 g2
"""

def make_set(g, nodes):
 """
  Returns a set with all nodes contained in the
  specified group. 
 """
 s = Set()
 names = nodes['names']
 for ii,name in enumerate(names):
  """ 
   We will assume node is entirely contained
   in group if they have one atom in common
  """ 
  atoms = mdn.dic2list(nodes[name]['atoms'])
  atom0 = atoms[0]
  if (atom0 in mdn.dic2list(g['atoms'])):
   s.add(ii)
 return s


ticket = sys.argv[1]
fname  = sys.argv[2]
g1     = sys.argv[3]
g2     = sys.argv[4]

data = mdn.get_data(ticket)

net = data['network']



gr1 = data['index']['groups'][g1]
gr2 = data['index']['groups'][g2]

nd1 = make_set(gr1, net['nodes'])
nd2 = make_set(gr2, net['nodes'])

nnodes = len(net['nodes']['names'])

wpath = np.zeros((nnodes,nnodes))


 


"""
 Double loop over all nodes to find out
 which pairs belong to g1 and g2
"""

for ii in range(nnodes):
 for jj in range(nnodes):
  if(ii in nd1 and jj in nd2 and ii != jj):
   wpath[ii][jj] = 1


np.save(fname, wpath)


  


