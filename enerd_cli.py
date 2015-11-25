import sys
import string
import re
import numpy as np
import mdn
import enerd

"""
 Usage: python enerd.py ticket
"""

"""
 Input files:
  enematrix -> output from gmxdump
  netindex -> .ndx file with node definitions
 Output file:
  enenpy -> energy matrix as numpy object
"""

enematrix = sys.argv[1]
netindex  = sys.argv[2]
enenpy    = sys.argv[3]
software  = sys.argv[4]

ener = enerd.do_core(netindex, enematrix, enenpy, software)



np.save(enenpy,ener)

