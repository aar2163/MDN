import sys
import string
import re


f = open(sys.argv[1],'r')

ngroups = 0

chosen = []
readchosen = 0

for line in f:
 #l = line.translate(string.maketrans("",""), string.punctuation).lower()
 #data = l.strip().split(" ")

 if(re.match(r'^\s*\[\s*\S+\s*\]\s*$',line)):
  readnode = 0
  readchosen = 0

  if(ngroups == int(sys.argv[3])):
   readchosen = 1

  ngroups += 1

 elif(readchosen == 1):
  l = line.strip()
  data = re.split(r'\s*',l)
  [chosen.append(i) for i in data]




f = open(sys.argv[2],'r')





nmol = 0

for i,line in enumerate(f):
 if(i > 1):
  l = line.translate(string.maketrans("",""), '\n')
  try: 
   anr = int(l[15:20])
   rnr = int(l[0:5])
  except:
   pass




