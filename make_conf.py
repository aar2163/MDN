import sys
import mdn
import re

excl_list = [r'^bincoordinates', r'coordinates', r'structure', \
             r'run', r'minimize', r'outputname', 'timestep', \
             r'fullElectFrequency', r'langevin', r'stepspercycle', \
             r'restartfreq', r'dcdfreq', r'xstfreq', r'outputenergies', \
             r'outputpressure', r'outputtiming']

data = mdn.get_data(sys.argv[1])

data['files']['energy_conf'] = data['base_dir'] + data['ticket'] \
                             + '-energy.conf'

if(data['software']['name'] == 'namd'):
 fname = data['base_dir'] + data['files']['configuration']['fname']
 f = open(fname, 'r')
 f2 = open(data['files']['energy_conf'], 'w')
 for line in f:
  bWrite = True
  for excl in excl_list:
   if(re.match(excl,line,re.IGNORECASE)):
    bWrite = False
  if(bWrite):
   f2.write(line)

 f2.write('margin 100000\n')
 f2.write('outputname energy\n')
 f2.write('coordinates '   + data['base_dir'] + data['files']['coordinates']['fname'] + '\n')
 f2.write('structure '     + data['base_dir'] + data['files']['structure']['fname'] + '\n')
 f2.write('parameters '    + data['base_dir'] + data['files']['parameters']['fname'] + '\n')
 f2.write('indexname '     + data['base_dir'] + data['files']['netindex_dat'] + '\n')
 f2.write('enematrixname ' + data['base_dir'] + data['files']['enematrix_dat'] + '\n')

 f2.write('coorfile open dcd ' + data['base_dir'] + data['files']['trajectory']['fname'] + '\n')

 string = 'while { ![coorfile read] } {\n' + \
  '# Set firstTimestep so our energy output has the correct TS.\n' + \
  'firstTimestep 1\n' + \
  '# Compute energies and forces, but don\'t try to move the atoms.\n' + \
  'run 0\n' + \
  'incr ts 1\n' + \
  '}\n'+ \
  'coorfile close\n'

 f2.write(string)

