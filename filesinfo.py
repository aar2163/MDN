import sys
import string
import re
import json
import mdn



data = mdn.get_data(sys.argv[1])

files = data['files']
names = files['names']

fnames = []

for ii,n in enumerate(names):
 f = files[n]
 upl = f['uploaded']
 if(upl):
  fname = f['fname']
  if(fname in fnames):
   continue
  else:
   fnames.append(fname)
 else:
  fname = 0

 print n,files[n]['title'],upl,fname,files[n]['extension']





  
