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

 

def do_nodes(data,fname):

 net = data['network']
 nodes = {}
 atoms_nr = []
 atoms_map = {}
 nodes_names = []
 readnode = False
 net['atoms'] = {}
 nnodes = 0
 bDAT = False

 top = data['topology']
 globatoms = mdn.do_globatoms(top)

 f = open(fname,'r')

 if(data['software']['name'] == 'namd'):
  bDAT = True
  netindex_dat = data['base_dir'] + data['files']['netindex_dat']
  f2 = open(netindex_dat, 'w')

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
 
 
    if bDAT:
     node_nr = re.split(r'_',last_node)[1]
     f2.write("{} {}\n".format(entry-1,node_nr))

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
 if(bDAT):
  f2.close()

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

def do_mdp(mdp1,mdp2):
 f = open(mdp1,'r')
 
 fout = open(mdp2,'w')
 
 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  l = lc[0]
 
 
  if not (re.match(r'^\s*energygrps',l)):
   #node = line.translate(string.maketrans("",""), '[]')
   #node = node.strip()
   #st = st + ' ' + node
   fout.write(line)
   
 f.close()
 
 fout.write(st.strip())
 
 fout.close()

## Main code


data = mdn.get_data(sys.argv[1])

netindex_ndx = data['base_dir'] + data['files']['netindex_ndx']


clear_mols(data)

st = do_nodes(data,netindex_ndx)

do_groups(data)




mdn.update_data(sys.argv[1],data)
  

if(data['software']['name'] == 'gromacs'):
 mdp1 = data['base_dir'] + data['files']['mdp']['fname']
 mdp2 = data['base_dir'] + data['files']['energy_mdp']
 do_mdp(mdp1,mdp2)




