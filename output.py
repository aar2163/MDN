import sys
import os
import re
import mdn
import zipfile


data = mdn.get_data(sys.argv[1])

ticket = data['ticket']

zf = zipfile.ZipFile(sys.argv[2],"w",zipfile.ZIP_DEFLATED)

for i in data['output_files']:
 base = os.path.basename(i)
 if(re.match(ticket,base)):
  st = re.split(ticket + '-',base)[1]
 else:
  st = base
 zf.write(i,st)

zf.close()


