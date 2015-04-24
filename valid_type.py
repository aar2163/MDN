import sys
import string
import re
import json
import mdn



data = mdn.get_data(sys.argv[1])

name = sys.argv[2]

files = data['files']
names = files['names']

if (name in names):
 for e in files[name]['extension']:
  print e
 exit()
else:
 print 1
 exit(1)






  
