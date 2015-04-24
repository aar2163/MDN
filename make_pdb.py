import sys
import string
import re


## MDN Server

## This script reads a CSV file listing atoms and the corresponding network property
## and a PDB file containing a biomolecule structure
## THE ATOM NUMBERING IN BOTH FILES MUST MATCH

## Command line: python make_pdb.py output.csv structure.pdb structure_new.pdb

## The output file structure_new.pdb will contain the values of the network property 
## in the occupancy field. This can be visualized with common visualization tools.


f = open(sys.argv[1])

eta = {}

for line in f:
 if(re.match(r'^\d+,\d+,\d+',line)):
  l = re.split(r',',line)
  eta[l[0]] = float(l[2])

f.close()


f = open(sys.argv[2])

fout = open(sys.argv[3],'w')

for line in f:
 if(re.match(r'^ATOM',line) or re.match(r'^HETATM',line)):
  a = str(int(line[6:11]))
  if(a in eta):
   line = line[0:54] + "{:6.2f}".format(eta[a]) + line[60:]
  fout.write(line)

f.close()
fout.close()






