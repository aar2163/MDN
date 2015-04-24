import sys
import string
import re
import json
import mdn


data = mdn.get_data(sys.argv[1])


print len(data['network']['nodes']['names'])





  
