import sys
import string
import re
import json
import os
import mdn

"""
 This script is called by files.php
 Usage: update_file.py ticket op typ fname
 Possible values:
 op: ['upload', 'download']
 typ: data['files']['names']
"""

def pop_entry(entry,data):
 if(entry in data):
  data.pop(entry,None)

def remove_required(files, typ):
 for i in files[typ]['required_files']:
  print i,names
  names.remove(i)
  try:
   fname = files[i]['fname']
   os.unlink(data['base_dir'] + fname)
  except:
   pass

  files.pop(i,None)
 files[typ].pop('required_files',None)


data = mdn.get_data(sys.argv[1])

ticket = data['ticket']


op = sys.argv[2] #upload or download

typ = sys.argv[3]

"""
 Auxiliary files, like ligand.itp, will contain the file extension.
 so we discard it
"""
typ = os.path.splitext(typ)[0]

fname = sys.argv[4]


files = data['files']
names = files['names']

if(op == 'upload'):
 files[typ]['uploaded'] = True
 files[typ]['fname'] = fname

if(op == 'delete'):
 files['upload_complete'] = False
 files[typ]['uploaded'] = False

 try:
  os.unlink(data['base_dir'] + fname)
 except:
  pass

 files[typ].pop('fname', None)

 if('required_files' in files[typ]):
  remove_required(files, typ)

 pop_entry('topology',data)
 pop_entry('index',data)
 pop_entry('network',data)
 pop_entry('output_files',data)



mdn.update_data(sys.argv[1],data)






  
