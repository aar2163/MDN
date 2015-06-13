import sys
import string
import re
import numpy as np
import json
import mdn




data = mdn.get_data(sys.argv[1])


data['base_dir'] = '/var/www/html/uploads/' + sys.argv[1] + '/'

data['validated'] = True

data['software'] = {}

data['software']['name'] = sys.argv[2]
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

if(sys.argv[2] == "gromacs"):

 data['software']['binpath'] = "/home/andre/gromacs463/bin"; 
 data['software']['top_dir'] = "/home/andre/gromacs463/share/gromacs/top/"

 files['names'] = ['coordinates','topology','mdp','trajectory','index']

 files['coordinates'] = {'title': 'Coordinates', 'mandatory': True, 'uploaded': False, 'extension': ['.gro']}
 files['topology'] = {'title': 'Topology', 'mandatory': True, 'uploaded': False, 'extension': ['.top']}
 files['mdp'] = {'title': 'MDP', 'mandatory': True, 'uploaded': False, 'extension': ['.mdp']}
 files['trajectory'] = {'title': 'Trajectory', 'mandatory': True, 'uploaded': False, 'extension': ['.xtc','.gro','.pdb','.trr','.trj']}
 files['index'] = {'title': 'Index', 'mandatory': True, 'uploaded': False, 'extension': ['.ndx']}


elif(sys.argv[2] == "namd"):

 data['software']['binpath'] = "/home/andre/NAMD_2.10_Source/Linux-x86_64-g++"; 

 files['names'] = ['coordinates','structure','configuration','parameters','trajectory','index']

 files['coordinates'] = {'title': 'Coordinates', 'mandatory': True, 'uploaded': False, 'extension': ['.pdb']}
 files['parameters'] = {'title': 'Parameters', 'mandatory': True, 'uploaded': False, 'extension': ['.inp', '.par']}
 files['structure'] = {'title': 'Structure', 'mandatory': True, 'uploaded': False, 'extension': ['.psf']}
 files['configuration'] = {'title': 'Configuration', 'mandatory': True, 'uploaded': False, 'extension': ['.conf']}
 files['trajectory'] = {'title': 'Trajectory', 'mandatory': True, 'uploaded': False, 'extension': ['.dcd']}
 files['index'] = {'title': 'Groups', 'mandatory': True, 'uploaded': False, 'extension': ['.ndx']}
 #files['extended'] = {'title': 'ExtendedSystem', 'mandatory': False, 'uploaded': False, 'extension': ['.xsc']}



else:
 print "Fatal error: invalid program"
 exit()
 

mdn.update_data(sys.argv[1],data)


