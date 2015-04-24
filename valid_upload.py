import sys
import string
import re
import json
import os
import mdn


data = mdn.get_data(sys.argv[1])

name = sys.argv[2]

fname = sys.argv[3]

files = data['files']
names = files['names']

bOk = True

if (name not in names):
 exit(1)

ext = os.path.splitext(fname)[1]
if (ext not in files[name]['extension']):
 exit(1)

if('check_name' in files[name]):
 bCheck = files[name]['check_name']
 if(bCheck):
  base = os.path.basename(fname)
  base = os.path.splitext(base)[0].upper()
  if(base != name):
   exit(1)

exit()


 






  
