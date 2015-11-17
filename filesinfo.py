import sys
import string
import re
import json
import mdn

"""
 Called by files.php
 Usage: python filesinfo.py ticket
"""

ticket = sys.argv[1]

data = mdn.get_data(ticket)

files = data['files']
names = files['names']

fnames = []

for n in range(len(names)):
 f = files[n]
 upl = f['uploaded']

 if (upl):
  fname = f['fname']

  if(fname in fnames):
   """
    This shouldn't be necessary, but it's here just in case
   """
   continue

  else:
   """
    Add fname to fnames array
   """
   fnames.append(fname)

 else:
  fname = 0

 """
  Print file information so files.php can read it
 """
 print n,files[n]['title'],upl,fname,files[n]['extension']





  
