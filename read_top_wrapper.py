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

"""
 Wrapper for read_top.py
 Only called by files.php
 Usage: python readtop.py ticket
"""


## Main code

ticket = sys.argv[1]

data = mdn.get_data(ticket)

read_top.read_top(data,True,True)

mdn.update_data(sys.argv[1],data)



