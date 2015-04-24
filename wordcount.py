import sys
import string

f = open(sys.argv[1],'r')

dic = {}

for line in f:
 l = line.translate(string.maketrans("",""), string.punctuation).lower()
 data = l.strip().split(" ")
 for d in data:
  if d in dic:
   dic[d] = dic[d] + 1
  else:
   dic[d] = 1

print dic
  
