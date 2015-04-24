import sys
import string
import re
import json
import os
import mdn
import read_top

### usage python check_files.py data.json

def check_molname(name,path):

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
   
  if(re.match(mdn.reanytype,line)):
   readmolname = False
  if(re.match(mdn.remoleculetype,line)):
   readmolname = True
 
 f.close()
 return bMatch

def do_atoms(atoms,name,path):

 f = open(path,'r')
 readatoms = False

 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
  if(readatoms and re.match(mdn.reatomline,line)):
   d = re.split(r'\s*',line)
   atoms['nr'].append(int(d[0]))
   atoms['resnr'].append(int(d[2]))
   
  
   
  if(re.match(mdn.reanytype,line)):
   if(readatoms):
    break
   readatoms = False
  if(re.match(mdn.reatoms,line)):
   readatoms = True
 
 f.close()

def do_bonds(atoms,residues,name,path):

 f = open(path,'r')
 readbonds = False

 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
  if(readbonds and re.match(mdn.rebondline,line)):
   d = re.split(r'\s*',line)
   idx1 = atoms['nr'].index(int(d[0]))
   idx2 = atoms['nr'].index(int(d[1]))
   r1 = atoms['resnr'][idx1]
   r2 = atoms['resnr'][idx2]

   if(r1 == r2):
    continue

   if(r2 not in residues[str(r1)]['bonds']):
    residues[str(r1)]['bonds'].append(r2)
   
   if(r1 not in residues[str(r2)]['bonds']):
    residues[str(r2)]['bonds'].append(r1)   
  
   
  if(re.match(mdn.reanytype,line)):
   readbonds = False
  if(re.match(mdn.rebonds,line)):
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


def do_top_gromacs(data):
 try: 
  top = data['topology']
 except:
  read_top.read_top(data,False,True)
  top = data['topology']

 topfiles = data['files']['topology']['required_files']
 mol_number = data['topology']['mol_number']
 mol_name   = data['topology']['mol_name']



 for name in mol_name:
  for key in topfiles:
   key = os.path.splitext(key)[0]
   f = files[key]['fname']
   path = data['base_dir'] + f
   bMatch = check_molname(name,path)
   if(bMatch):
    mol = top[name] = {}
    mol['fname'] = f
    mol['atoms'] = {}
    mol['atoms']['nr'] = []
    mol['atoms']['resnr'] = []
    do_atoms(mol['atoms'],name,path)

    mol['residues'] = {}
    mol['residues']['resnr'] = []
    do_residues(mol['atoms'],mol['residues'])

    do_bonds(mol['atoms'],mol['residues'],name,path)
    break

def do_top(data,output):

 if(data['software']['name'] == 'namd'):
  do_top_pdb(data)

 if(data['software']['name'] == 'gromacs'):
  do_top_gromacs(data)


 #######
 #print topfiles
 #globatoms = do_global(top)

 nmol = 0

 mol_number = data['topology']['mol_number']
 mol_name   = data['topology']['mol_name']

 for n in mol_number:
  nmol += n

  output.append("The topology lists {} molecules:\n".format(nmol))

 for i,n in enumerate(data['topology']['mol_number']):
  output.append("{}: {}\n".format(data['topology']['mol_name'][i],n))


def do_index(data,output):

 index = {}

 index['specified_nodes'] = False
 
 index['groups'] = {}
 index['groups']['nr'] = []
 index['groups']['names'] = []
 
 #index['atoms'] = {}
 
 ngroups = 0
 
 
 readgroup = False
 
 fname = data['files']['index']['fname']
 
 path = data['base_dir'] + fname
 
 f = open(path,'r')
 
 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
 
  if (re.match(mdn.reanytype,line)):
   readgroup = True
   group = line.translate(string.maketrans("",""), '[]')
   group = group.strip()
   if (re.match(mdn.renode,group)):
    index['specified_nodes'] = True
   index['groups']['nr'].append(ngroups)
   index['groups']['names'].append(group)
   index['groups'][str(ngroups)] = {}
   index['groups'][str(ngroups)]['atoms'] = []
   ngroups += 1
  elif (readgroup and re.match(mdn.reindexline,line)):
   d = re.split(r'\s*',line)
   for entry in d:
    entry = int(entry)
    index['groups'][str(ngroups-1)]['atoms'].append(entry)
 
 
 for nr in index['groups']['nr']:
  index['groups'][str(nr)]['atoms'] = mdn.list2dic(index['groups'][str(nr)]['atoms'])
 
 data['index'] = index

 output.append("The index file lists {} groups\n".format(ngroups))


def check_groups(groups,globatoms):  
 for group in groups['nr']:
  bOk = True
  groupatoms = mdn.dic2list(groups[str(group)]['atoms'])
  nres = 0
  for a in groupatoms:
   try:
    lp = l
    l  = globatoms[str(a)]
    lgp = globatoms[str(a-1)]
 
    if(mdn.same_residue(l,lgp)):
     if (mdn.same_residue(l,lp)):
      if(lgp[0] != lp[0]):
       bOk = False
     else:
      bOk = False
    else:
     nres += 1
     if(nres > mdn.max_nnodes):
      bOk = False
     
   except:
    l = globatoms[str(a)]
  ###
  groups[str(group)]['network_ok'] = bOk



  


### Main code


data = mdn.get_data(sys.argv[1])

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
 files['upload_complete'] = True

#PrevStatus = False  # testing only (will analyze topology regardless of status)

output = []

if(estat == 0 and not PrevStatus):
 do_top(data,output)
 do_index(data,output)
 globatoms = mdn.do_globatoms(data['topology'])
 check_groups(data['index']['groups'],globatoms)
 #check_input
 data['network'] = {}
 data['network']['available'] = True
 data['files']['upload_log'] = output





mdn.update_data(sys.argv[1],data)

exit(estat)  



 






  
