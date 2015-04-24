import sys
import string
import re
from sets import Set
import numpy as np
import json
import os.path
import shutil
import mdn

def add_required(top,fname):
 if('required_files' not in top):
  top['required_files'] = []

 if(fname not in top['required_files']):
  top['required_files'].append(fname)
 #print 'hey',top['required_files']

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


def read_top(data,dofiles,dotop):

 # Reads topology and (optionally) adds file entries to data
 # bool dofiles controls file writing

 ticket = data['ticket']
 
 gromacs_dir = data['gromacs_dir']
 
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
 
  if(re.match(mdn.remoleculetype,line)):

   if(dofiles):
    name = upper_name(top['fname'])
    add_file(files,name,'.top')
    files[name]['uploaded'] = True
    files[name]['fname'] = top['fname']

   if(dotop and dofiles):
    add_required(top,name)
   
  if(re.match(mdn.reinclude,line)):
   finc = re.split(r'\s*',line)[1]
   finc = finc.translate(string.maketrans("",""), '\"')
   bfinc = os.path.basename(finc)
   #name = os.path.splitext(bfinc)[0].upper()
   name = upper_name(bfinc)
   ext  = os.path.splitext(bfinc)[1]
 
 
   if(dofiles):
    add_file(files,name,ext)
   
   if(dotop and dofiles):
    add_required(top,name)
    
   default_file = gromacs_dir + finc
   if(dofiles and os.path.isfile(default_file)):
    shutil.copy(default_file,base_dir+bfinc)
    files[name]['uploaded'] = True
    files[name]['fname'] = bfinc
 
  if(readmol and re.match(mdn.renameval,line)):
   d = re.split(r'\s*',line)
   mol_name.append(d[0])
   mol_number.append(int(d[1]))
   
  if(re.match(mdn.reanytype[software],line)):
   readmol = False
  if(re.match(mdn.remolecules,line)):
   readmol = True
 
 f.close()
 
 if(dotop):
  data['topology'] = {}
  data['topology']['mol_name'] = mol_name
  data['topology']['mol_number'] = mol_number





