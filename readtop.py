import sys
import string
import re
from sets import Set
import numpy as np
import json
import os.path
import shutil
import read_top
import mdn



## Main code

data = mdn.get_data(sys.argv[1])

read_top.read_top(data,True,True)

mdn.update_data(sys.argv[1],data)



