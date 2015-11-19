import numpy as np
import sys
import string
import re
import mdn

"""
 Calculates internode distances and writes output DAT files

 Called by analysis.php
 Usage: python centrality.py adj wpath ref_enerd enerd adj_dat wpath_dat dist_dat");
 Input files: adj wpath enerd enerd2
 Output files: adj_dat wpath_dat dist_dat
"""

bEner = True
bCorr = False

data = mdn.get_data(sys.argv[1])

adj       =  np.load(sys.argv[2])
wpath     =  np.load(sys.argv[3])
ref_ener  = -np.load(sys.argv[4])
ener      = -np.load(sys.argv[5])

adj_dat   = sys.argv[6]
wpath_dat = sys.argv[7]
dist_dat  = sys.argv[8]


ind1 = (adj == 0)
ind2 = (ref_ener > 1)
ind3 = (ener != 0)

"""
 Find out which nodes are not covalently bound
 and have negative interaction energies in the reference matrix
"""
ref_intersect = ind1*ind2

"""
 Find out which nodes are not covalently bound
 and have non-zero interaction energies in the system energy matrix 
"""
intersect = ind1*ind3


d1 = ener[intersect]
d2 = ref_ener[ref_intersect]

try:
 mean = data['network']['params']['mean']
 prms = data['network']['params']['std']
except:
 mean = np.mean(d2)
 prms = np.std(d2, ddof=1)

#mean = 10.0
#prms = 15.0

ener[intersect] -= mean
ener[intersect] /= 5.0 * prms
ener[intersect] += 1.0
ener[intersect] *= 0.5

ind = ener < 0.01
ener[ind] = 0.0
ind = ener > 0.99
ener[ind] = 0.99








bEner = True
bCorr = False



nnodes = len(ref_ener)

weight = np.zeros((nnodes,nnodes))

if(bEner):
 weight[:] = 0.99
 weight[ind1] = ener[ind1]
else:
 weight[ind1] = 0

dist = weight.copy()

ind_d = (dist != 0)
dist[ind_d] = -np.log(abs(weight[ind_d]))


"""
 Write output DAT files
"""

fout = open(adj_dat, 'w')
for i in adj.flatten():
 line = "{}\n".format(i)
 fout.write(line)
fout.close()

fout = open(wpath_dat, 'w')
for i in wpath.flatten():
 line = "{}\n".format(i)
 fout.write(line)
fout.close()

fout = open(dist_dat, 'w')
for i in dist.flatten():
 line = "{}\n".format(i)
 fout.write(line)
fout.close()



