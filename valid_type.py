import sys
import string
import re
import json
import mdn

"""
 Called by files.php
 Usage: python valid_type.py ticket typ
"""

ticket = sys.argv[1]
typ    = sys.argv[2]

data = mdn.get_data(ticket)


files = data['files']
names = files['names']

if (typ in names):
 """
  valid type, so print possible file extensions
 """
 for e in files[typ]['extension']:
  print e
 exit()

else:
 """
  exit with error
 """
 print 1
 exit(1)






  
