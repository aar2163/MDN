import sys
import os
import re
import mdn
import zipfile

"""
 Called by analysis.php
 Usage: python output.py ticket zip_fn
"""

ticket = sys.argv[1]
zip_fn = sys.argv[2]

data = mdn.get_data(ticket)

zf = zipfile.ZipFile(zip_fn,"w",zipfile.ZIP_DEFLATED)

"""
 Loop over all output files specified in the database
 and add to zipfile
"""
for i in data['output_files']:
 base = os.path.basename(i)

 if(re.match(ticket,base)):
  st = re.split(ticket + '-',base)[1]

 else:
  st = base

 zf.write(i,st)

zf.close()


