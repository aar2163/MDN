import sys
import string
import re
import numpy as np
import json
import mdn

"""
 Called by prepenecore.php
 Usage: python nodes.py ticket
"""

def clear_mols(data):
 """
  This should not be necessary, but it's here 
  just in case. Remove all node information from 
  topology entry
 """
 for name in data['topology']['mol_name']:
  try:
   data['topology'][name].pop('netnodes',None)
  except:
   pass

 

def do_nodes(data,fname):

 """
  Reads netindex file, with nodes specified as groups 
  for energy analysis
 """

 net = data['network']

 """
  Initialize some variables
 """
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

 """ 
  st will have the gromacs mdp line specifying
  node energy groups
 """ 
 st = "energygrps ="

 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
 
  if (re.match(mdn.reanytype['gromacs'], line)):
   readnode = False
 
  if (re.match(mdn.renode_strict, line)):
   """
    Check if this line has a node name
    renode_strict is necessary here, not sure why
   """
   readnode = True
   nnodes += 1

   """
    Get node name
   """
   node = line.translate(string.maketrans("",""), '[]')
   node = node.strip()


   """ 
    Check if node name is invalid 
   """  
   if(node == 'names' or node == 'nr'):
    print("Fatal error: You cannot have a group named {}\n".format(node))
    exit(1)

   """  
    Update mdp string and add this node to list
   """  
   st = st + ' ' + node
   last_node = node
   nodes_names.append(node)
 
  elif(readnode and re.match(r'^\s*\d+',line)):
   """
    Reading node atoms
   """
   d = re.split(r'\s*',line)
   for entry in d:
    entry = int(entry)
 
    atoms_nr.append(entry)
 
 
    if bDAT:
     node_nr = re.split(r'_',last_node)[1]
     f2.write("{} {}\n".format(entry-1,node_nr)) #NAMD index = GROMACS index - 1

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

 for ii, n in enumerate(names):
  """  
   Get node index
  """  
  idx = nr[ii]
  group = groups[str(idx)]
  atoms = mdn.dic2list(group['atoms'])

  bInclude = True

  """ 
   Check if all atoms of this group are part
   of the network
  """ 
  for a in atoms:
   if (a not in netatoms):
    bInclude = False

  """ 
   Print results for debugging purposes
  """ 
  print idx, n, bInclude
  group['bNetwork'] = bInclude



def do_mdp(mdp1, mdp2, st):
 f = open(mdp1,'r')
 
 fout = open(mdp2,'w')
 
 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  l = lc[0]
 
 
  """
   Copying lines from mdp1 to mdp2
   We skip any energygrps
   We also set coulombtype to cutoff
   and cutoff-sheme to group 
  """

  if not (re.match(r'^\s*energygrps',l)):
   if re.search(r'coulombtype\s*=\s*pme',l.lower()):
    line = "coulombtype = cutoff\n"
   if re.search(r'cutoff-scheme\s*=\s*verlet',l.lower()):
    line = "cutoff-scheme = group\n"

   fout.write(line)
   
 f.close()
 
 fout.write(st.strip())
 
 fout.close()



def main():

 data = mdn.get_data(sys.argv[1])

 netindex_ndx = data['base_dir'] + data['files']['netindex_ndx']


 clear_mols(data)

 st = do_nodes(data, netindex_ndx)

 do_groups(data)




 mdn.update_data(sys.argv[1],data)
  

 if(data['software']['name'] == 'gromacs'):
  mdp1 = data['base_dir'] + data['files']['mdp']['fname']
  mdp2 = data['base_dir'] + data['files']['energy_mdp']
  do_mdp(mdp1,mdp2, st)



if __name__ == '__main__':
 main()




