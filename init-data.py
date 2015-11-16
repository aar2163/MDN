import sys
import string
import re
import numpy as np
import json
import mdn



"""
 This script is only called by validate.php
 Usage: init-data.py ticket software
"""

ticket = sys.argv[1]

# Possible values of software
possible_software = ['gromacs', 'namd']
software = sys.argv[2]


data = mdn.get_data(ticket)


data['base_dir'] = '/var/www/html/uploads/' + ticket + '/'

data['validated'] = True

data['software'] = {}

data['software']['name'] = software
data['software']['gromacs_bindir'] = "/home/andre/gromacs463/bin/"

data['files'] = {}

files = data['files']

files['upload_complete'] = False

files['netindex_ndx']  = data['ticket'] + '-netindex.ndx'
files['netindex_dat']  = data['ticket'] + '-netindex.dat'
files['energy_conf']   = data['ticket'] + '-energy.conf'
files['energy_mdp']   = data['ticket'] + '-energy.mdp'
files['enematrix_dat'] = data['ticket'] + '-enematrix.dat'
files['enerd_npy']     = data['ticket'] + '-enerd.npy'

if not software in possible_software:
 print "Fatal error: invalid software name"
 exit()



if(software == "gromacs"):

 data['software']['binpath'] = "/home/andre/gromacs463/bin"; 
 data['software']['top_dir'] = "/home/andre/gromacs463/share/gromacs/top/"

 files['names'] = ['coordinates','topology','mdp','trajectory','index']

 files['coordinates'] = {'title': 'Coordinates', 'mandatory': True, 'uploaded': False, 'extension': ['.gro']}
 files['topology'] = {'title': 'Topology', 'mandatory': True, 'uploaded': False, 'extension': ['.top']}
 files['mdp'] = {'title': 'MDP', 'mandatory': True, 'uploaded': False, 'extension': ['.mdp']}
 files['trajectory'] = {'title': 'Trajectory', 'mandatory': True, 'uploaded': False, 'extension': ['.xtc','.gro','.pdb','.trr','.trj']}
 files['index'] = {'title': 'Index', 'mandatory': True, 'uploaded': False, 'extension': ['.ndx']}


elif(software == "namd"):

 data['software']['binpath'] = "/home/andre/NAMD_2.10_Source/Linux-x86_64-g++"; 

 files['names'] = ['coordinates','structure','configuration','parameters','trajectory','index']

 files['coordinates'] = {'title': 'Coordinates', 'mandatory': True, 'uploaded': False, 'extension': ['.pdb']}
 files['parameters'] = {'title': 'Parameters', 'mandatory': True, 'uploaded': False, 'extension': ['.inp', '.par']}
 files['structure'] = {'title': 'Structure', 'mandatory': True, 'uploaded': False, 'extension': ['.psf']}
 files['configuration'] = {'title': 'Configuration', 'mandatory': True, 'uploaded': False, 'extension': ['.conf']}
 files['trajectory'] = {'title': 'Trajectory', 'mandatory': True, 'uploaded': False, 'extension': ['.dcd']}
 files['index'] = {'title': 'Groups', 'mandatory': True, 'uploaded': False, 'extension': ['.ndx']}
 #files['extended'] = {'title': 'ExtendedSystem', 'mandatory': False, 'uploaded': False, 'extension': ['.xsc']}



mdn.update_data(ticket, data)


