import numpy as np
import sys
import string
import re

bEner = True
bCorr = False


adj = np.load(sys.argv[1])

wpath = np.load(sys.argv[2])

ener = -np.load(sys.argv[3])
ener2 = -np.load(sys.argv[4])
#ener3 = -np.load(sys.argv[4])


ind1 = (adj == 0)
ind2 = (ener > 1)
ind3 = (ener2 != 0)
#ind4 = (ener3 != 0)

intersect = ind1*ind2
intersect2 = ind1*ind3
#intersect3 = ind1*ind4


d1 = ener2[intersect2]
d2 = ener[intersect]

mean = np.mean(d2)
prms = np.std(d2,ddof=1)

mean = 10.0
prms = 15.0


ener2[intersect2] -= mean
ener2[intersect2] /= 5*prms
ener2[intersect2] += 1.0
ener2[intersect2] *= 0.5

ind = ener2 < 0.01
ener2[ind] = 0.0
ind = ener2 > 0.99
ener2[ind] = 0.99
#print ener








#log = sys.argv[5]

bEner = True
bCorr = False



nnodes = len(ener)

weight = np.zeros((nnodes,nnodes))
#weight2 = np.zeros((nnodes,nnodes))

if(bEner):
 weight[:] = 0.99
 #weight2[:] = 0.99
 weight[ind1] = ener2[ind1]
else:
 weight[ind1] = 0

dist = weight.copy()
ind1 = (dist != 0)
dist[ind1] = -np.log(abs(weight[ind1]))


fout = open(sys.argv[5],'w')
for i in adj.flatten():
 line = "{}\n".format(i)
 fout.write(line)
fout.close()

fout = open(sys.argv[6],'w')
for i in wpath.flatten():
 line = "{}\n".format(i)
 fout.write(line)
fout.close()

fout = open(sys.argv[7],'w')
for i in dist.flatten():
 line = "{}\n".format(i)
 fout.write(line)
fout.close()



