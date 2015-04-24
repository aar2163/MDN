import sys
import string
import re
from sets import Set
import numpy as np
import json
import mdn

def make_set(l,nodes):
 s = Set()
 names = nodes['names']
 for ii,name in enumerate(names):
  atoms = mdn.dic2list(nodes[name]['atoms'])
  atom0 = atoms[0]
  if (atom0 in mdn.dic2list(l['atoms'])):
   s.add(ii)
 return s


data = mdn.get_data(sys.argv[1])

net = data['network']


chosen1 = sys.argv[3]
chosen2 = sys.argv[4]

l1 = data['index']['groups'][chosen1]
l2 = data['index']['groups'][chosen2]

nnodes = len(net['nodes']['names'])

atoms_nr = mdn.dic2list(net['atoms']['nr'])


wpath = np.zeros((nnodes,nnodes))

nd1 = make_set(l1,net['nodes'])
nd2 = make_set(l2,net['nodes'])

 



for ii in range(nnodes):
 for jj in range(nnodes):
  if(ii in nd1 and jj in nd2 and ii != jj):
   wpath[ii][jj] = 1


np.save(sys.argv[2],wpath)


  


