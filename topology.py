import sys
import string
import re
from sets import Set
import numpy as np


f = open(sys.argv[2],'r')

nnodes = 0

alist = Set()
readchosen = 0
nodemap = {}

for line in f:
 lc = re.split(r';',line.strip())  # removing comments
 line = lc[0]

 if(re.match(r'^\s*\[\s*\S+\s*\]\s*$',line)):
  readnode = 0


 if(re.match(r'^\s*\[\s*Node_\d+\s*\]\s*$',line)):
  readnode = 1
  nnodes += 1
 elif(readnode == 1 and re.match(r'\d+',line)):
  l = line.strip()
  data = re.split(r'\s*',l)
  for entry in data:
   alist.add(int(entry))
   nodemap[int(entry)] = nnodes-1

f.close()

bonded = np.zeros((nnodes,nnodes)) ## chemical bonds, (ii,jj) is 1 if pair is bound, 0 otherwise




f = open(sys.argv[3],'r')


mol_name = []
mol_number = []

readmol = 0

nmol = 0

for line in f:
 lc = re.split(r';',line.strip())  # removing comments
 line = lc[0]

 if(readmol == 1 and re.match(r'^\s*\w+\s+\d+\s*$',line)):
  data = re.split(r'\s*',line)
  mol_name.append(data[0])
  mol_number.append(int(data[1]))
  nmol += 1
 if(re.match(r'^\s*\[\s*\w+\s*\]\s*$',line)):
  readmol = 0
 if(re.match(r'^\s*\[\s*molecules\s*\]\s*$',line)):
  readmol = 1

f.close()

mol_natom = []

prev_natom = 0 

gnode = Set()

ngnode = {}


mol_name_d = {}

for ii in range(len(mol_name)):
 if(ii > 0):
  try: 
   prev_natom += mol_natom[ii-1]*mol_number[ii-1]
  except:
   pass
 for jj in range(4,len(sys.argv)):

  inp = sys.argv[jj]
  f = open(inp,'r')

  readtype = 0
  readatom = 0
  readbond = 0

  for line in f:

   lc = re.split(r';',line.strip())  # removing comments
   line = lc[0]

   if(readtype == 1 and re.match(r'^\s*\w+\s+\d+\s*$',line)):
    data = re.split(r'\s*',line)
    if (data[0] != mol_name[ii]):
     lala = 0
     break
    else:
     mol_name_d[inp] = mol_name[ii]
     lala = 1

   if(readatom == 1 and re.match(r'^\s*\d+',line)):
    data = re.split(r'\s*',line)
    atom = prev_natom + int(data[0])
    try: 
     mol_natom[ii] += 1
    except:
     mol_natom.append(1)
    if(atom in alist):
     nodeid = nodemap[atom]
     if(nodeid not in gnode):
      gnode.add(nodeid)
      try:
       ngnode[inp] += 1
      except:
       ngnode[inp] = 1

   if(readbond == 1 and re.match(r'^\s*\d+',line)):
    data = re.split(r'\s*',line)
    atom0 = prev_natom + int(data[0])
    atom1 = prev_natom + int(data[1])
    if(atom0 in alist and atom1 in alist):
     nd0 = nodemap[atom0]
     nd1 = nodemap[atom1]
     if(nd0 != nd1):
      bonded[nd0][nd1] = 1
      bonded[nd1][nd0] = 1

   if(re.match(r'^\s*\[\s*\S+\s*\]\s*$',line)):
    readtype = 0
    readatom = 0
    readbond = 0

   if(re.match(r'^\s*\[\s*moleculetype\s*\]\s*$',line)):
    readtype = 1

   if(re.match(r'^\s*\[\s*atoms\s*\]\s*$',line)):
    readatom = 1

   if(re.match(r'^\s*\[\s*bonds\s*\]\s*$',line)):
    readbond = 1
       

  f.close()


np.save(sys.argv[1],bonded)

print("Total nodes: {}\n".format(nnodes))

for jj in range(4,len(sys.argv)):
 f = sys.argv[jj]
 print("{}: {} nodes\n".format(mol_name_d[f],ngnode[f]))

