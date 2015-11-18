import sys
import string
import re
import numpy as np
import mdn

"""
 Called by prepenecore.php
 Usage: python enerd.py ticket
"""

readnode = 0
nnodes = 0

index = {}


data = mdn.get_data(sys.argv[1])


"""
 Input files:
  enematrix -> output from gmxdump
  netindex -> .ndx file with node definitions
 Output file:
  enenpy -> energy matrix as numpy object
"""

enematrix = data['base_dir'] + data['files']['enematrix_dat']
netindex  = data['base_dir'] + data['files']['netindex_ndx']
enenpy    = data['base_dir'] + data['files']['enerd_npy']



f = open(netindex,'r')

for line in f:
 lc = re.split(r';',line.strip())  # removing comments
 line = lc[0]

 if (re.match(mdn.renode_strict,line)):
  """
   Get node name
  """
  node = mdn.get_node_name(line)

  """
   Set index as current number of nodes
  """
  index[node] = nnodes

  nnodes += 1

f.close()

ener = np.zeros((nnodes,nnodes))



f = open(enematrix,'r')

for line in f:
 lc = re.split(r';',line.strip())  # removing comments
 line = lc[0]

 if(data['software']['name'] == 'gromacs'):
  if (re.match(mdn.redouble_node, line)):
   """
    Found line that specifies node-node energy
   """
   v = re.split(r'\s+',line)
   value = float(v[1])
   s = re.split(r':',v[0])[1] # we just want the second element (Node_x-Node_y)
   n = re.split(r'-',s)

   try:
    id0 = index[n[0]]
    id1 = index[n[1]]
    ener[id0,id1] += value
    ener[id1,id0] += value
   except:
    pass

 elif(data['software']['name'] == 'namd'):
  """
   NAMD energy output was already written in the required format
   We need to convert energy to kJ/mol
  """
  v = re.split(r'\s+',line)
  v0 = int(v[0])
  v1 = int(v[1])
  v2 = float(v[2])*4.184
  ener[v0][v1] = v2
  ener[v1][v0] = v2
 


np.save(enenpy,ener)

