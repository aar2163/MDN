import sys
import string
import re
import json
import mdn



data = mdn.get_data(sys.argv[1])

name = sys.argv[2]

print data['files'][name]['fname']





  
