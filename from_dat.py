import numpy as np
import sys
import re
import math

def get_effic(a,b):
 a = a.flatten()
 b = b.flatten()
 a = a[a != -1]
 b = b[b != -1]
 return np.sum(a)/np.sum(b)


a = []
with open(sys.argv[1],'r') as f:
 for line in f:
  l = re.split(r'\s',line.strip())
  #print l[0],l[1]
  a.append(float(l[0]))

nnodes = int(math.sqrt(len(a)))

ener = np.zeros((nnodes,nnodes))

print nnodes

for i in range(len(a)):
  rest = (i % nnodes)
  n = int(float(i)/nnodes)
  #print a[i],effic
  ener[n][rest]   = a[i]

np.save('teste.npy',ener)
