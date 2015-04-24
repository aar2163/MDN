import sys
import string
import re
import numpy as np
import mdn

readnode = 0
nnodes = 0

index = {}


data = mdn.get_data(sys.argv[1])

enematrix = data['base_dir'] + data['files']['enematrix_dat']
netindex  = data['base_dir'] + data['files']['netindex_ndx']
enenpy    = data['base_dir'] + data['files']['enerd_npy']



f = open(netindex,'r')

for line in f:
 lc = re.split(r';',line.strip())  # removing comments
 line = lc[0]

 #if (re.match(r'^\s*\[\s*w+\s*\]\s*$',line)):
 # readnode = 0
 if (re.match(r'^\s*\[\s*Node_\d+\s*\]\s*$',line)):
  node = line.translate(string.maketrans("",""), '[]')
  node = node.strip()
  index[node] = nnodes
  nnodes += 1

f.close()

ener = np.zeros((nnodes,nnodes))



f = open(enematrix,'r')

for line in f:
 lc = re.split(r';',line.strip())  # removing comments
 line = lc[0]

 if(data['software']['name'] == 'gromacs'):
  if (re.match(r'\S*:Node_\d+-Node_\d+',line)):
   v = re.split(r'\s+',line)
   value = float(v[1])
   s = re.split(r':',v[0])[1] # we just want the second element (Node_x-Node_y)
   n = re.split(r'-',s)
   #print n[0],n[1],float(v[1])
   try:
    id0 = index[n[0]]
    id1 = index[n[1]]
    ener[id0,id1] += value
    ener[id1,id0] += value
   except:
    pass

 elif(data['software']['name'] == 'namd'):
  v = re.split(r'\s+',line)
  v0 = int(v[0])
  v1 = int(v[1])
  v2 = float(v[2])*4.184
  ener[v0][v1] = v2
  ener[v1][v0] = v2
 


np.save(enenpy,ener)

