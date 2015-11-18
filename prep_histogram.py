import sys
import numpy as np
import json
import mdn

"""
 Writes JSON string with energy histogram info
 Usage: python prep_histogram.py ticket
"""

ticket = sys.argv[1]

data = mdn.get_data(ticket)

base_dir = data['base_dir']

enerd = np.load(base_dir + data['files']['enerd_npy'])

try:
 adj = np.load(base_dir + data['files']['adj_npy'])
except:
 """ 
  Old database entries do not have adj_npy defined
 """ 
 adj = np.load(base_dir + ticket + '-adj.npy')

ind1 = (enerd != 0)
ind2 = (adj == 0)

intersect = ind1*ind2

non_zero = enerd[intersect]

hist, edges = np.histogram(non_zero, bins=20, range=(-100,100))

output = {}
output['hist']  = hist.tolist()
output['edges'] = edges.tolist()

print json.dumps(output)


