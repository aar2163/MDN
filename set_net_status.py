import sys
import string
import re
import json
import mdn



data = mdn.get_data(sys.argv[1])

bTrue = (sys.argv[3].lower() == 'true')

data['network'][sys.argv[2]] = bTrue


mdn.update_data(sys.argv[1],data)





  
