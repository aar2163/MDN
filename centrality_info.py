import numpy as np
import sys
import re
import math
import mdn
from sets import Set

def get_effic(a,b):
 a = a.flatten()
 b = b.flatten()
 a = a[a != -1]
 b = b[b != -1]
 return np.sum(a)/np.sum(b)

data = mdn.get_data(sys.argv[1])

groups = data['index']['groups']
names = groups['names']
chosen = data['network']['chosen_group']

#netset = Set(mdn.dic2list(groups[chosen]['atoms']))
netset = Set(mdn.dic2list(data['network']['atoms']['nr']))

for ii,n in enumerate(names):
 s = Set(mdn.dic2list(groups[str(ii)]['atoms']))

 if (re.match(mdn.renode,n)):
  continue
 print ii,n,(s.issubset(netset) and  groups[str(ii)]['network_ok'])
 #if(ii == 18):
 # print s


  
