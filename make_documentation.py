from lxml import html
import requests
import re
from urlparse import urlparse
import os.path

class Stack:
 def __init__(self):
  self.items = []
 def push(self,item):
  self.items.append(item)
 def pop(self):
  self.items.pop()
 def size(self):
  return len(self.items)

def process_ul(ul):
 column = []
 for i in ul:
  text = i.text_content()
  text = re.sub(r'_',r'\_',text)
  text = re.sub(r'#','\#',text)
  column.append(text)
 return column

def get_columns(div):
 columns = []
 for i in div:
  if i.tag == 'div':
   columns = columns + get_columns(i)
  if i.tag == 'ul':
   column = process_ul(i)
   columns.append(column)
 
 return columns

def do_table(columns):
 if len(columns) > 0:
  print '\\begin{table}[H]'
  print '\centering'
  string = []
  [string.append('c') for i in columns]
  string = '|'.join(string)
  print '\\begin{tabular}{' + string + '}'
  print '\hline'

  for i in range(len(columns[0])):
   row = []
   for j in columns:
    row.append(j.pop(0))
   print ' & '.join(row) + '\\' + '\\'

  print '\end{tabular}'
  print '\end{table}'

def process_img(p):
 for i in p:
  if i.tag == 'img':
   if 'latex' in i.attrib and i.attrib['latex'] == 'hide':
    pass
   else:
    src = urlparse(i.attrib['src'])
    fname = os.path.basename(src.path)
    print '\\begin{figure}[H]'
    print '\includegraphics[width=3.5in]{' + fname + '}'
    print '\end{figure}'

def process_url(url):
   
 page = requests.get(url)
 tree = html.fromstring(page.text)

 for i in tree.body:
  if i.tag == 'div':
   columns = get_columns(i)
   do_table(columns)

  
  if i.tag == 'h1':
   section = i.text_content()
   print '\section{' + section + '}'
  if(i.tag == 'p'):
   process_img(i)
   attrib = i.attrib
   text = i.text_content()
   text = re.sub(r'_',r'\_',text)
   text = re.sub(r'#','\#',text)
   if 'latex' in attrib and attrib['latex'] == 'hide':
    continue
   if 'latex' in attrib and attrib['latex'] == 'subsection':
    print '\subsection{' + text + '}'
   else:
    print text + "\n"
 



f = open('latex_template.tex','r')

for line in f:
 print line.strip()

sections = Stack()

url = ['http://mdn.cheme.columbia.edu/documentation/file-upload.php', \
       'http://mdn.cheme.columbia.edu/documentation/choosing-groups.php', \
       'http://mdn.cheme.columbia.edu/documentation/creating-groups.php', \
       'http://mdn.cheme.columbia.edu/documentation/custom-nodes.php', \
       'http://mdn.cheme.columbia.edu/documentation/network-construction.html', \
       'http://mdn.cheme.columbia.edu/documentation/pathways.html', \
       'http://mdn.cheme.columbia.edu/documentation/output.html']

[process_url(i) for i in url]

appendices = ['http://mdn.cheme.columbia.edu/documentation/file-size.php', \
              'http://mdn.cheme.columbia.edu/documentation/network-analysis.php']

print "\\begin{appendices}"
[process_url(i) for i in appendices]
print "\\end{appendices}"

print "\end{document}"
