import sys
import string
import re
import json
import mdn


data = mdn.get_data(sys.argv[1])

groups = data['index']['groups']
names = groups['names']

if not data['index']['specified_nodes']:
 for ii,n in enumerate(names):
  """
  f = files[n]
  upl = f['uploaded']
  if(upl):
   fname = f['fname']
  else:
   fname = 0
  """

  #print n,files[n]['title'],upl,fname
  print ii,n,groups[str(ii)]['network_ok']
else:
 print 0,'SPECIFIED_NODES',True






  
