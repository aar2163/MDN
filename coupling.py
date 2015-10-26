import numpy as np
import sys
import re
import math
import mdn
from sets import Set

def add_output(fname,output_files):
 if(fname not in output_files):
  output_files.append(fname)

def get_effic(a,b,idx1,idx2):
 a = a[np.ix_(idx1,idx2)]
 b = b[np.ix_(idx1,idx2)]
 a = a.flatten()
 b = b.flatten()
 a = a[a != -1]
 b = b[b != -1]
 return np.sum(a)/np.sum(b)

def get_nodeset(data):
 names = data['network']['nodes']['names']
 s = []
 for i in names:
  s.append(Set(mdn.dic2list(data['network']['nodes'][i]['atoms'])))
 return s

def get_nodes(atoms,nodeset):
 s = Set(atoms)
 n = []
 for ii,i in enumerate(nodeset):
  #print len(atoms), ii, i.issubset(s)
  #if i.issubset(s) or data['index']['specified_nodes']:
  if i.issubset(s):
   n.append(ii)
 return n

def get_nodelist(valid,nodeset):

 nodelist = []
 for i in valid:
  atoms = mdn.dic2list(data['index']['groups'][str(i)]['atoms'])
  j = get_nodes(atoms,nodeset)
  nodelist.append(j)
 return nodelist



data = mdn.get_data(sys.argv[1])


valid = mdn.valid_groups_for_analysis(data,False)


nodeset = get_nodeset(data)


nodelist = get_nodelist(valid,nodeset)




a = []
b = []
with open(sys.argv[2],'r') as f:
 for line in f:
  l = re.split(r'\s',line.strip())
  #print l[0],l[1]
  a.append(float(l[0]))
  b.append(float(l[1]))

nnodes = int(math.sqrt(len(a)))



effic = np.zeros((nnodes,nnodes))
efficid = np.zeros((nnodes,nnodes))

for i in range(len(a)):
  rest = (i % nnodes)
  n = int(float(i)/nnodes)
  #print a[i],effic
  if(rest >= n):
   effic[n][rest]   = a[i]
   efficid[n][rest] = b[i]
   effic[rest][n]   = a[i]
   efficid[rest][n] = b[i]

fname = data['base_dir'] + data['ticket'] + '-coupling.log'


add_output(fname,data['output_files'])

with open(fname,'w') as f:

 glob = get_effic(effic,efficid,nodelist[0],nodelist[0])

 #f.write("Global: {}\n\n".format(glob)) #global is ill-defined in some cases

 for ii,i in enumerate(valid):
  iname = data['index']['groups']['names'][i]
  for jj,j in enumerate(valid):
   if(j >= i):
    jname = data['index']['groups']['names'][j]
    f.write("{} - {}: {}\n".format(iname,jname,get_effic(effic,efficid,nodelist[ii],nodelist[jj])))
  f.write("\n")

atoms = []



globatoms = mdn.do_globatoms(data['topology'])

for ii,i in enumerate(valid):
 iname = data['index']['groups']['names'][i]
 fname = data['base_dir'] + data['ticket'] + '-coupling-' + iname + '.csv'

 """
 add_output(fname,data['output_files'])

 with open(fname,'w') as f:
  bLast = False
  f.write("Atom Number,Residue Size,Coupling\n")
  for j in mdn.dic2list(data['network']['atoms']['nr']):
   d1 = globatoms[str(j)]

   try:
    d2 = globatoms[str(j+1)]
   except:
    bLast = True
   
   atoms.append(j)

   if not mdn.same_residue(d1,d2) or bLast == True:
    node = get_nodes(atoms,nodeset)
    value = get_effic(effic,efficid,node,nodelist[ii])
    for k in atoms:
     f.write("{},{},{}\n".format(k,len(atoms),value))
    atoms = []
 """

 for hh,h in enumerate(valid):
  if h == i:
   continue
  hname = data['index']['groups']['names'][h]
  fname = data['base_dir'] + data['ticket'] + '-coupling-' + iname + '-' + hname + '.csv'
  add_output(fname,data['output_files'])
  #print iname,hname

  with open(fname,'w') as f:
   bLast = False
   f.write("Atom Number,Residue Size,Coupling\n")
   for j in mdn.dic2list(data['index']['groups'][str(h)]['atoms']):
    d1 = globatoms[str(j)]

    try:
     d2 = globatoms[str(j+1)]
    except:
     bLast = True
   
    atoms.append(j)

    if not mdn.same_residue(d1,d2) or bLast == True:
     node = get_nodes(atoms,nodeset)
     value = get_effic(effic,efficid,node,nodelist[ii])
     #print value
     for k in atoms:
      f.write("{},{},{}\n".format(k,len(atoms),value))
     atoms = []


mdn.update_data(sys.argv[1],data)

  
