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

def print_img(fname, caption = None):
 if not fname:
  return

 print '\\begin{figure}[H]'
 print '\includegraphics[width=3.5in]{' + fname + '}'

 if caption:
  print '\caption{ \
    {\\bf ' + caption + '} \
}'

 print '\end{figure}'

def get_img_fname(i):
 fname = None
 if i.tag == 'img':
  if 'latex' in i.attrib and i.attrib['latex'] == 'hide':
   pass
  else:
   src = urlparse(i.attrib['src'])
   fname = os.path.basename(src.path)
 return fname

def process_img(p):
 caption = None
 for i in p:
  if i.tag == 'img':
   fname = get_img_fname(i)
   print_img(fname)

  if i.tag == 'figure':
   for j in i:
    if j.tag == 'img':
     fname = get_img_fname(j)
    if j.tag == 'figcaption':
     caption = j.text_content()
     print_img(fname, caption)
   p.remove(i)
 return caption

def process_url(url,appendices=False):
   
 page = requests.get(url)
 tree = html.fromstring(page.text)

 if appendices:
  level_1 = '\section{' 
  level_2 = '\subsection{' 
 else:
  level_1 = '\subsection{' 
  level_2 = '\subsubsection{' 

 for i in tree.body:
  if i.tag == 'div':
   columns = get_columns(i)
   do_table(columns)

  
  if i.tag == 'h1':
   section = i.text_content()
   print level_1 + section + '}'
  if(i.tag == 'p'):
   caption = process_img(i)
   attrib = i.attrib
   text = i.text_content()
   text = re.sub(r'_',r'\_',text)
   text = re.sub(r'#','\#',text)
   if 'latex' in attrib and attrib['latex'] == 'hide':
    continue
   if 'latex' in attrib and attrib['latex'] == 'subsection':
    print level_2 + text + '}'
   else:
    print text + "\n"
 



f = open('latex_template.tex','r')

for line in f:
 print line.strip()

sections = Stack()

print "\\section{Main Steps}"

main_steps = ['http://mdn.cheme.columbia.edu/documentation/file-upload.php', \
              'http://mdn.cheme.columbia.edu/documentation/network-construction.php', \
              'http://mdn.cheme.columbia.edu/documentation/pathways.php', \
              'http://mdn.cheme.columbia.edu/documentation/output.php']

[process_url(i) for i in main_steps]

print "\\section{The Index File}"

the_index = ['http://mdn.cheme.columbia.edu/documentation/choosing-groups.php', \
             'http://mdn.cheme.columbia.edu/documentation/creating-groups.php']

[process_url(i) for i in the_index]

appendices = ['http://mdn.cheme.columbia.edu/documentation/file-size.php', \
              'http://mdn.cheme.columbia.edu/documentation/network-analysis.php']

print "\\begin{appendices}"
[process_url(i,appendices=True) for i in appendices]
print "\\end{appendices}"

print "\end{document}"
