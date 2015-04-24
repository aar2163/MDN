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
  
   


reatomline =     r'^\s*\d+\s+\w+\S*\s+\d+\s*'
reindexline =    r'^\s*\d+'
rebondline =     r'^\s*\d+\s+\d+\s*\d+'
renameval =      r'^\s*\w+\S*\s+\d+\s*$'
reanytype =      r'^\s*\[\s*\S+\s*\]\s*$'
remoleculetype = r'^\s*\[\s*moleculetype\s*\]\s*$'
reinclude =      r'^\#include'
remolecules =    r'^\s*\[\s*molecules\s*\]\s*$'
reatoms =        r'^\s*\[\s*atoms\s*\]\s*$'
rebonds =        r'^\s*\[\s*bonds\s*\]\s*$'
