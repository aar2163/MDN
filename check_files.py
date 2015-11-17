import sys
import string
import re
import json
import os
import mdn
import read_top
from sets import Set

"""
 This script is only called by files.php

 Usage: python check_files.py ticket
"""

def check_molname(name, path, software):

 """
  Only relevant for gromacs jobs
  Reads .top or .itp and checks if it is the molname we are looking for
 """

 f = open(path,'r')
 readmolname = False
 bMatch = False

 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
  if(readmolname and re.match(mdn.renameval,line)):
   d = re.split(r'\s*',line)
   molname = d[0]
   if(molname == name):
    bMatch = True
    break
  

  """
   Check if we are reading the moleculetype specification section
   Format:
    [ moleculetype ]
     molname nrexcl
  """
  if(re.match(mdn.reanytype[software],line)):
   readmolname = False
  if(re.match(mdn.remoleculetype,line)):
   readmolname = True
 
 f.close()
 return bMatch

def do_atoms(atoms,path,software):

 """
  Relevant for both gromacs and namd
 """

 f = open(path,'r')
 readatoms = False

 res = Set()

 corr_res = 0

 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
  # Check whether it's an atom line
  if(readatoms and re.match(mdn.reatomline[software],line)):
   d = re.split(r'\s+',line)
   atoms['nr'].append(int(d[0]))

   r = int(d[2])
   if(corr_res + r < len(res)):
    corr_res = len(res)

   res.add(r)

   atoms['resnr'].append(corr_res + r)
   
  
   
  """
   Check if we are reading the atom specification section
   Format GROMACS:
    [ atoms ]
     atom1 ...
     atom2 ...
  """
  if(re.match(mdn.reanytype[software],line)):
   if(readatoms):
    break
   readatoms = False
  if(re.match(mdn.reatoms[software],line)):
   readatoms = True
 
 f.close()

def add_bond(i,j,atoms,residues):
 idx1 = atoms['nr'].index(i)
 idx2 = atoms['nr'].index(j)
 r1 = atoms['resnr'][idx1]
 r2 = atoms['resnr'][idx2]


 if(r1 == r2):
  return


 if(r2 not in residues[str(r1)]['bonds']):
  residues[str(r1)]['bonds'].append(r2)
 
 if(r1 not in residues[str(r2)]['bonds']):
  residues[str(r2)]['bonds'].append(r1)   

def do_bonds(atoms,residues,path,software):

 f = open(path,'r')
 readbonds = False

 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
  if(readbonds and re.match(mdn.rebondline[software],line)):
   d = re.split(r'\s+',line)
   add_bond(int(d[0]),int(d[1]),atoms,residues)

   if(software == 'namd'):
    if(len(d) > 2):
     add_bond(int(d[2]),int(d[3]),atoms,residues)
    if(len(d) > 4):
     add_bond(int(d[4]),int(d[5]),atoms,residues)
    if(len(d) > 6):
     add_bond(int(d[6]),int(d[7]),atoms,residues)
  
   
  if(re.match(mdn.reanytype[software],line)):
   readbonds = False
  if(re.match(mdn.rebonds[software],line)):
   readbonds = True
 
 f.close()

def do_residues(atoms,residues):
 for ii,a in enumerate(atoms['nr']):
  resnr = atoms['resnr'][ii]
  if(resnr not in residues['resnr']):
   residues['resnr'].append(resnr)
   residues[str(resnr)] = {}
   residues[str(resnr)]['atoms'] = []
   residues[str(resnr)]['bonds'] = []

  residues[str(resnr)]['atoms'].append(a)

def do_top_pdb(data):
 #Makes topology based on PDB file
 #Entire system is considered one molecule

 f = data['files']['coordinates']['fname']
 path = data['base_dir'] + f
 fo = open(path,'r')

 top = data['topology'] = {}

 #Create one molecule named system
 top['mol_name'] = ['system']
 top['mol_number'] = [1]
 mol = top['system'] = {} 

 atoms = mol['atoms'] = {}
 atoms['nr'] = []
 atoms['resnr'] = []

 atom = 0

 for line in fo:
  if(re.match(mdn.repdb_atom, line)):
   atom += 1
   #The sum is necessary as PDB atom serial number
   #is not reliable for large molecules

   res = int(line[22:26])
   atoms['nr'].append(atom)
   atoms['resnr'].append(res)

 mol['residues'] = {}
 mol['residues']['resnr'] = []
 do_residues(mol['atoms'],mol['residues'])

def do_top_psf(data):
 #Makes topology based on PSF file
 #Entire system is considered one molecule

 f = data['files']['structure']['fname']
 path = data['base_dir'] + f
 fo = open(path,'r')

 software = data['software']['name']

 top = data['topology'] = {}

 #Create one molecule named system
 top['mol_name'] = ['system']
 top['mol_number'] = [1]
 mol = top['system'] = {} 

 atoms = mol['atoms'] = {}
 atoms['nr'] = []
 atoms['resnr'] = []


 do_atoms(mol['atoms'],path,software)

 mol['residues'] = {}
 mol['residues']['resnr'] = []
 do_residues(mol['atoms'],mol['residues'])

 do_bonds(mol['atoms'],mol['residues'],path,software)


def do_top_gromacs(data):
 try: 
  top = data['topology']
 except:
  # This should not be necessary, but here just in case
  read_top.read_top(data,False,True)
  top = data['topology']

 # get all topology files .top and .itp
 topfiles = data['files']['topology']['required_files']

 mol_number = data['topology']['mol_number']
 mol_name   = data['topology']['mol_name']

 software = data['software']['name']



 for name in mol_name:
  for key in topfiles:
   key = os.path.splitext(key)[0]
   f = files[key]['fname']
   path = data['base_dir'] + f

   # check if it's the molecule we want to process
   bMatch = check_molname(name, path, software)
   if(bMatch):
    mol = top[name] = {}
    mol['fname'] = f
    mol['atoms'] = {}
    mol['atoms']['nr'] = []
    mol['atoms']['resnr'] = []
    do_atoms(mol['atoms'],path,software)

    mol['residues'] = {}
    mol['residues']['resnr'] = []

    # Read residues and bonds

    do_residues(mol['atoms'],mol['residues'])

    do_bonds(mol['atoms'],mol['residues'],path,software)

    # done, so don't need to check other files
    break

def do_top(data,output):

 if(data['software']['name'] == 'namd'):
  do_top_psf(data)

 if(data['software']['name'] == 'gromacs'):
  do_top_gromacs(data)

 nmol = 0

 mol_number = data['topology']['mol_number']
 mol_name   = data['topology']['mol_name']

 for n in mol_number:
  nmol += n

  output.append("The topology lists {} molecules:\n".format(nmol))

 for i,n in enumerate(data['topology']['mol_number']):
  output.append("{}: {}\n".format(data['topology']['mol_name'][i],n))



def make_new_group(index, ngroups, group):
 index['groups']['nr'].append(ngroups)
 index['groups']['names'].append(group)
 index['groups'][str(ngroups)] = {}
 index['groups'][str(ngroups)]['atoms'] = []


def do_index(data,output):

 index = {}

 index['specified_nodes'] = False
 
 index['groups'] = {}
 index['groups']['nr'] = []
 index['groups']['names'] = []
 
 ngroups = 0
 
 readgroup = False
 
 # get path of index file
 fname = data['files']['index']['fname']

 software = data['software']['name']
 
 path = data['base_dir'] + fname
 
 f = open(path,'r')

 inodes = -1
 nnodes = -1

 node_atoms = {}
 
 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
 
  if (re.match(mdn.reanytype['gromacs'], line)): #index file is always gromacs
   readgroup = True
   readnode = False
   read_node_group = False

   # get group from '[ group ]'
   group = line.translate(string.maketrans("",""), '[]')
   group = group.strip()

   # Check if group is a node
   if (re.match(mdn.renode, group)):

    """
     If group is node, we create group SPECIFIED_NODES if it has not been created
     We will add all node atoms to this group
     inodes variable should store the index of this group
    """
    index['specified_nodes'] = True
    readnode = True
    nnodes += 1

    if(inodes == -1): #first time reading a node
     inodes = ngroups
     make_new_group(index, ngroups, 'SPECIFIED_NODES')
     ngroups += 1

   else:
    make_new_group(index, ngroups, group)
    ngroups += 1
    if re.match(mdn.renode_group, group):
     read_node_group = True

  elif (readgroup and re.match(mdn.reindexline, line)):
   # if we read the group name on the last line, now it's time to store the atoms

   # group atom lines should be single-space separated integers
   d = re.split(r'\s*',line)

   for entry in d:
    entry = int(entry)

    if not readnode and not read_node_group:

     # Standard group: append atom index to group

     index['groups'][str(ngroups-1)]['atoms'].append(entry)

    elif read_node_group:

     # Node group, so indexes refer to nodes, not atoms
     # and we need a loop over the corresponding atoms

     for atom in node_atoms[str(entry)]:
      index['groups'][str(ngroups-1)]['atoms'].append(atom)
    else:

     # Node: append atom index to node specification

     index['groups'][str(inodes)]['atoms'].append(entry)

     if not str(nnodes) in node_atoms:
      node_atoms[str(nnodes)] = []

     node_atoms[str(nnodes)].append(entry)
      
 
 
 # Now go over all groups and save atom list in optimized format
 for nr in index['groups']['nr']:
  index['groups'][str(nr)]['atoms'] = mdn.list2dic(index['groups'][str(nr)]['atoms'])
 
 data['index'] = index

 output.append("The index file lists {} groups\n".format(ngroups))


def check_groups(groups,globatoms):  
 for group in groups['nr']:
  bOk = True
  """
   network_ok will be True only if all residues are complete or 
   we are using SPECIFIED_NODES
  """

  # Convert stored atom list to full array
  groupatoms = mdn.dic2list(groups[str(group)]['atoms'])

  nres = 0
  for a in groupatoms:
   try:
    """
     this fails for the first atom
     for the remaining atoms we can compare residues
     Note that atom indices are local to the molecule, so we need to use globatoms
     globatoms format : [atom_number,residue_number,molecule_name,molecule,number]
    """
   

    lp = l
    l  = globatoms[str(a)]
    lgp = globatoms[str(a-1)]
 
    if(mdn.same_residue(l,lgp)):
     if (mdn.same_residue(l,lp)):
      if(lgp[0] != lp[0]):
       # This enforces global(a-1) = global(a) - 1
       bOk = False
     else:
      # This catches group definitions that do not include the whole residue
      bOk = False
    else:
     # if current atom is not in same residue as previous atom, increase nres
     nres += 1
     if(nres > mdn.max_nnodes):
      bOk = False
     
   except:
    l = globatoms[str(a)]

  ###
  name = groups['names'][group]
  groups[str(group)]['network_ok'] = bOk or (name == 'SPECIFIED_NODES')
  groups[str(group)]['network_specified'] = True if re.match(mdn.renode_group,name) else False



  


### Main code

ticket = sys.argv[1]

data = mdn.get_data(ticket)

files = data['files']
names = files['names']

estat = 0


if('upload_complete' not in files):
 files['upload_complete'] = False

PrevStatus = files['upload_complete']


if not files['upload_complete']:
 for n in names:
  if(files[n]['uploaded'] == False):
   files['upload_complete'] = False
   estat = 1


if(estat == 0):
 CurrStatus = True
 files['upload_complete'] = True
else:
 CurrStatus = False


ForceAnalysis = False

output = []

"""
 Check if file upload is complete AND
 this has just happened
"""

if (CurrStatus and (not PrevStatus or ForceAnalysis)):
 errors = []
 # Process topology first
 try:
  do_top(data,output)
 except:
  errors.append('topology')

 # Now do index file
 try:
  do_index(data,output)

  """
   Note that atom indices are local to the molecule, so we need to use globatoms
  """
  globatoms = mdn.do_globatoms(data['topology'])

  # Loop over all groups, and find if they should be available for network setup
  check_groups(data['index']['groups'], globatoms)
 except:
  errors.append('index')

 #check_input
 data['network'] = {}
 data['network']['available'] = True

 if len(errors) > 0:
  estat = 2
  data['network']['available'] = False
  s = ''
  for i in errors:
   s = s + i + ' '
  output = [s]

 data['files']['upload_log'] = output





mdn.update_data(ticket, data)

"""
 estat is 0 if file_upload is complete AND 
 do_top and do_index were successful
"""
exit(estat)  



 






  
