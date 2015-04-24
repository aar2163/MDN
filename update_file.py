import sys
import string
import re
import json
import os
import mdn

def pop_entry(entry,data):
 if(entry in data):
  data.pop(entry,None)

def remove_required(files,name):
 for i in files[name]['required_files']:
  print i,names
  names.remove(i)
  try:
   fname = files[i]['fname']
   os.unlink(data['base_dir']+fname)
  except:
   pass

  files.pop(i,None)
 files[name].pop('required_files',None)


data = mdn.get_data(sys.argv[1])

ticket = data['ticket']


op = sys.argv[2] #upload or download

name = sys.argv[3]
name = os.path.splitext(name)[0]

fname = sys.argv[4]


files = data['files']
names = files['names']

if(op == 'upload'):
 files[name]['uploaded'] = True
 files[name]['fname'] = fname

if(op == 'delete'):
 files['upload_complete'] = False
 files[name]['uploaded'] = False

 try:
  os.unlink(data['base_dir'] + fname)
 except:
  pass

 files[name].pop('fname',None)

 if('required_files' in files[name]):
  remove_required(files,name)

  """
  for i in files[name]['required_files']:
   print i,names
   names.remove(i)
   try:
    fname = files[i]['fname']
    os.unlink(data['base_dir']+fname)
   except:
    pass

   files.pop(i,None)
  files[name].pop('required_files',None)
  """

 pop_entry('topology',data)
 pop_entry('index',data)
 pop_entry('network',data)
 pop_entry('output_files',data)


 #if(files[name]['mandatory'] == False):
 # files.pop(name,None)


mdn.update_data(sys.argv[1],data)






  
