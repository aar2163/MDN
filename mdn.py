import json
from sets import Set
from pymongo import MongoClient
import re

reatomline = {}
reatomline['gromacs'] =     r'^\s*\d+\s+\w+\S*\s+\d+\s+'
reatomline['namd']    =     r'^\s*\d+\s+\w+\S*\s+\d+\s+'

reindexline =    r'^\s*\d+'

rebondline = {}
rebondline['gromacs'] =   r'^\s*\d+\s+\d+\s+\d+'
rebondline['namd']    =   r'^\s*\d+\s+\d+\s+\d+'


renameval =      r'^\s*\w+\S*\s+\d+\s*$'

reanytype = {}
reanytype['gromacs'] =   r'^\s*\[\s*\S+\s*\]\s*$'
reanytype['namd']    =   r'^\s*\d+\s+!'


remoleculetype = r'^\s*\[\s*moleculetype\s*\]\s*$'
reinclude =      r'^\#include'
remolecules =    r'^\s*\[\s*molecules\s*\]\s*$'

reatoms = {}
reatoms['gromacs'] =     r'^\s*\[\s*atoms\s*\]\s*$'
reatoms['namd']    =     r'^\s*\d+\s+!NATOM'

rebonds = {}
rebonds['gromacs'] =     r'^\s*\[\s*bonds\s*\]\s*$'
rebonds['namd']    =     r'^\s*\d+\s+!NBOND'

renode  =        r'^\s*Node\_'
renode_group  =        r'^\s*NodeGroup\_'
repdb_atom =     r'^ATOM|^HETATM'

max_nnodes = 2000

def same_residue(l1,l2):

 if(l1[1] == l2[1] and \
    l1[2] == l2[2] and \
    l1[3] == l2[3]):
  return True
 else:
  return False

def list2dic(l):
 dic = {}
 for ii,a in enumerate(l):
  if(ii == 0):
   first = a
  if(ii > 0 and a != aprev + 1):
   dic[str(first)] = aprev
   first = a
  aprev = a
 dic[str(first)] = aprev  ##last segment
 return dic

def dic2list(dic):
 l = []
 m = map(int, dic.keys())
 for k in sorted(m):
  [l.append(i) for i in range(k,dic[str(k)]+1)]
 return l

def get_data(ticket):
 #js = open(f,'r')
 #data = json.load(js)
 #js.close()

 client = MongoClient()
 
 db = client.MDN

 data = db.jobs.find_one({'ticket': ticket})

 client.close()

 return data

def update_data(ticket,data):
 #f = "uploads/" + str(ticket) + "/" + str(ticket) + "-data.json"
 #js = open(f,'w')
 #json.dump(data,js)
 #js.close()

 client = MongoClient()
 
 db = client.MDN

 db.jobs.update({'ticket': data['ticket']},data,upsert=True)

 client.close()

def valid_groups_for_analysis(data,bPrint):
 groups = data['index']['groups']
 names = groups['names']
 chosen = data['network']['chosen_group']

 netset = Set(dic2list(groups[str(chosen)]['atoms']))

 valid = []

 for ii,n in enumerate(names):
  s = Set(dic2list(groups[str(ii)]['atoms']))
  cond = (s.issubset(netset) and groups[str(ii)]['network_ok'] and not re.match(renode,n))
  if(bPrint):
   print ii,n,cond
  if(cond):
   valid.append(ii)
 return valid

def do_globatoms(top):
 
 globatoms = {}
 
 mol_name = top['mol_name']
 mol_number = top['mol_number']

 count = 0
 for ii,name in enumerate(mol_name):
  for jj in range(mol_number[ii]):
   for kk,nr in enumerate(top[name]['atoms']['nr']):
    idx = count + 1
    count += 1
    #globatoms['nr'].append(idx)

    idx = str(idx)
    globatoms[idx] = []  ## globatoms : [atom_number,residue_number,molecule_name,molecule,number]
    globatoms[idx].append(nr)
    globatoms[idx].append(top[name]['atoms']['resnr'][kk])
    globatoms[idx].append(name)
    globatoms[idx].append(jj)

 return globatoms

  
   


