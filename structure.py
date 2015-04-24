import sys
import string
import re
import numpy as np
import json
import mdn

def clear_mols(data):
 ## This should not be necessary
 for name in data['topology']['mol_name']:
  try:
   data['topology'][name].pop('netnodes',None)
  except:
   pass

 

def do_nodes(net,fname):

 net = data['network']
 nodes = {}
 atoms_nr = []
 atoms_map = {}
 nodes_names = []
 readnode = False
 net['atoms'] = {}
 nnodes = 0

 top = data['topology']
 globatoms = top['global']['atoms']

 f = open(fname,'r')

 st = "energygrps ="

 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
 
  if (re.match(r'^\s*\[\s*\S+\s*\]\s*$',line)):
   readnode = False
 
  if (re.match(r'^\s*\[\s*Node_\d+\s*\]\s*$',line)):
   readnode = True
   nnodes += 1
   node = line.translate(string.maketrans("",""), '[]')
   node = node.strip()
   if(node == 'names' or node == 'nr'):
    print("Fatal error: You cannot have a group named {}\n".format(node))
    exit(1)
   
   st = st + ' ' + node
   last_node = node
   nodes_names.append(node)
 
  elif(readnode and re.match(r'^\s*\d+',line)):
   d = re.split(r'\s*',line)
   for entry in d:
    entry = int(entry)
 
    atoms_nr.append(entry)
 
 
    try: 
     nodes[last_node]['atoms'].append(entry)
    except:
     nodes[last_node] = {}
     nodes[last_node]['atoms'] = []
     nodes[last_node]['atoms'].append(entry)
     l = globatoms[str(entry)][:]
     nodes[last_node]['globres'] = l
 
     mol_name = l[2]
     mol = top[mol_name]
 
     if ('netnodes' in mol):
      mol['netnodes'] += 1
     else:
      mol['netnodes'] = 1

 f.close()

 net['nodes'] = nodes
 net['nodes']['names']   = nodes_names
 net['atoms']['nr']   = mdn.list2dic(atoms_nr)

 for name in nodes_names:
  net['nodes'][name]['atoms'] = mdn.list2dic(net['nodes'][name]['atoms'])  
 return st

def do_groups(data):
 groups = data['index']['groups']
 names = groups['names']
 nr = groups['nr']
 netatoms = mdn.dic2list(data['network']['atoms']['nr'])

 for ii,n in enumerate(names):
  idx = nr[ii]
  group = groups[str(idx)]
  atoms = mdn.dic2list(group['atoms'])
  bInclude = True
  for a in atoms:
   if (a not in netatoms):
    bInclude = False
  print idx,n,bInclude
  group['bNetwork'] = bInclude

## Main code


data = mdn.get_data(sys.argv[1])

ticket = data['ticket']

inp = data['base_dir'] + data['files']['coordinates']['fname']

f = open(inp,'r')

#globatoms = data['topology']['global']['atoms']


netatoms = mdn.dic2list(data['network']['atoms']['nr'])

num_lines = sum(1 for line in open(inp))

saved = []

nincluded = 0

for ii,line in enumerate(f):
 if(ii > 1 and ii < num_lines-1):
  a = ii-1
  #print line
  if (a in netatoms):
   nincluded += 1
   saved.append(line)
 else:
  saved.append(line)
 #if a in netatoms:
 # print line

if(nincluded != len(netatoms)):
 print "Fatal error: coordinates file does not contain the entire network"
 exit(1)

f.close()

saved[1] = "{}\n".format(nincluded)

out = data['base_dir'] + data['ticket'] + '-network.gro'

f = open(out,'w')

for i in saved:
 f.write(i)

f.close()


nodes = data['network']['nodes']

#for i in nodes['names']:
# print nodes[i].keys()







