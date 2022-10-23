import os
import time
import re

of = input('Please enter the address of the file to be processed:')
nf = input('Please enter the new file address:')
nn = input('Please enter the new file name(No suffix is required):')

aname = ''
if nn in aname:
    localtime = time.localtime(time.time())
    time = time.strftime('%Y%M%D%H%M%S', time.localtime(time.time()))
    time = time.replace('/', '')
    nn = time

suffix = '.ltml'
name = os.path.join(nn, suffix)
name = name.replace('\\', '')
nnf = os.path.join(nf, name)
print(nnf)

tf1 = 'TF1.ltml'  # Temporary files1
tf1 = os.path.join(nf, tf1)

tf2 = 'TF2.ltml'  # Temporary files2
tf2 = os.path.join(nf, tf2)

f = open(of)
t1 = open(tf1, 'w')
t2 = open(tf2, 'w')

'''
try:  # t1
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        if line.count('\n') == len(line):
            continue
        t1.write(line)
        t2.write(line)
finally:
    f.close()
    t1.close()
    t2.close()
    print('--- File generated ---')
'''
for line in f.readlines():  # t1
    if line == '\n':
        line = line.strip('\n')
    t1.write(line)

f.close()
tf1.close()
tf2.close()
print('--- File generated ---')

with open(nnf, 'a') as f:
    f.write('<!ltml version="1.0">\n<!subset="tml">\n')  # Write the version of the ltml and the subset

    '''
    The code here is used to extract the retrieval characters and English interpretations from the target file,
    as well as Chinese interpretations of the retrieved characters.
    '''
    ex = open(tf1, 'r+')

    line = ex.readline()
    ex.seek(0)

    while line:
        un = u'[\u4e00-\u9fff,\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\u300a\u300b\u2026]+'
        w = re.findall(un, line)
        ww = ''.join(w)
        afline = line[line.rfind(ww):]  # Extract all characters after ww
        afline = afline.replace(ww, '')
        afline = afline.strip()  # Remove both ends of the space
        # print(afline)
        beline = line[0:line.rfind(ww):]  # Extract all characters before ww
        beline = beline.replace(ww, '')
        beline = beline.strip()
        # print(beline)
        bSECmark = '<Section>'
        bWORDmark = '<Word>'
        eWORDmark = '</Word>'
        bTEmark = '<TraEN>'
        eTEmark = '</TraEN>'
        bTCmark = '<TraCN>'
        eTCmark = '</TraCN>'
        eSECmark = '</Section>'
        sec = [bSECmark, bWORDmark, beline, eWORDmark, bTEmark, afline, eTEmark, bTCmark, ww, eTCmark, eSECmark]
        secw = ''.join(sec)
        print(secw, file=f)
        line = ex.readline()

    ex.close()
    print('--- Refactoring write complete ---')

os.remove(tf1)
os.remove(tf2)
print('--- All operations are complete ---')

# Code end
