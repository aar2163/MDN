import json
from pymongo import MongoClient
import os

name = "ions.itp"

name = os.path.splitext(name)[0]
print name


