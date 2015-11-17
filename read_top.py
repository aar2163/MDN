import sys
import string
import re
from sets import Set
import numpy as np
import json
import os.path
import shutil
import mdn

"""
 Imported by read_top_wrapper.py and check_files.py,
 calling read_top function
"""

def add_required(top,fname):
 if('required_files' not in top):
  top['required_files'] = []

 if(fname not in top['required_files']):
  top['required_files'].append(fname)

def add_file(files,fname,ext):
 try:
  files[fname]['title'] = fname
 except:
  files[fname] = {}
  files['names'].append(fname)
  files[fname]['title'] = fname
 
 files[fname]['mandatory'] = False
 files[fname]['uploaded'] = False
 files[fname]['check_name'] = True
 files[fname]['extension'] = [ext]

def upper_name(fname):
 return os.path.splitext(fname)[0].upper()


def read_top(data, dofiles, dotop):

 """
   Reads topology and (optionally) adds file entries to data
   bool dofiles controls file writing
   
   Called by read_top_wrapper.py (data, True, True) when topology file is first uploaded,
   and again by check_files.py (data, False, True) upon completion of file upload step
 """

 ticket = data['ticket']

 """
  Find out directory containing default topology files
 """
 top_dir = data['software']['top_dir']
 
 base_dir = data['base_dir']
 
 files = data['files']
 
 top = files['topology']
 
 topfname = base_dir + top['fname']

 software = data['software']['name']
 
 f = open(topfname,'r')
 
 readmol = False
 
 
 mol_name = []
 mol_number = []
 
 for line in f:
  lc = re.split(r';',line.strip())  # removing comments
  line = lc[0]
 
  if(re.match(mdn.remoleculetype, line)):

   if(dofiles):
    """
     This is True when called by the wrapper after topology file upload
     All molecules  should have their own file, so if there is a molecule
     listed in the .top file we "create" a file for it and list it as uploaded
    """
    name = upper_name(top['fname'])
    add_file(files, name, '.top')
    files[name]['uploaded'] = True
    files[name]['fname'] = top['fname']

   if(dotop and dofiles):
    add_required(top,name)
   
  if(re.match(mdn.reinclude,line)):
   """
    If the topology includes any .itp files, we need to keep track of it
   """
   finc = re.split(r'\s*',line)[1]
   finc = finc.translate(string.maketrans("",""), '\"')
   bfinc = os.path.basename(finc)
   name = upper_name(bfinc)
   ext  = os.path.splitext(bfinc)[1]
 
 
   if (dofiles):
    """
     Add this file, but do not say it has been uploaded
     User will need to do this
    """
    add_file(files, name, ext)
   
   if(dotop and dofiles):
    """
     Uploading these auxiliary files is mandatory
    """
    add_required(top,name)
    
   """
     Find out if this file can be found in top_dir
   """
   default_file = top_dir + finc

   if(dofiles and os.path.isfile(default_file)):
    """
     If we can, list it as uploaded, and copy it to
     user directory
    """
    shutil.copy(default_file,base_dir+bfinc)
    files[name]['uploaded'] = True
    files[name]['fname'] = bfinc
 
  if(readmol and re.match(mdn.renameval,line)):
   """
    Reading molecules section, so add the
    corresponding number of molecules of each type
   """
   d = re.split(r'\s*',line)
   mol_name.append(d[0])
   mol_number.append(int(d[1]))
   
  if(re.match(mdn.reanytype[software],line)):
   readmol = False
  if(re.match(mdn.remolecules,line)):
   readmol = True
 
 f.close()
 
 if(dotop):
  """
   Note: this is being done both with the wrapper and check_files, 
         which is probably unnecessary
  """
  data['topology'] = {}
  data['topology']['mol_name'] = mol_name
  data['topology']['mol_number'] = mol_number





