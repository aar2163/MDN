import sys
import string
import re
import json
import os
import mdn

"""
 Called by files.php
 Usage: python valid_upload.py ticket typ fname
"""

ticket = sys.argv[1]
typ    = sys.argv[2]
fname  = sys.argv[3]

data = mdn.get_data(ticket)

files = data['files']
names = files['names']

bOk = True

if (typ not in names):
 exit(1)

"""
 Get file extension
"""
ext = os.path.splitext(fname)[1]

if (ext not in files[typ]['extension']):
 exit(1)

if ('check_name' in files[typ]):

 """
  Auxiliary files included by read_top should be
  checked for matching file name
 """
 bCheck = files[typ]['check_name']

 if(bCheck):
  base = os.path.basename(fname)
  base = os.path.splitext(base)[0].upper()

  """
   File type for auxiliary files is always set to upper case
  """

  if(base != typ):
   exit(1)

exit()


 






  
