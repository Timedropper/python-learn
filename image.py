#!/data/data/com.termux/files/usr/bin/python
import numpy as np
from sys import argv
from PIL import Image
string = [
        '[]', '{}', '€€', '#1', '%%', '77', '**', '==',
        '++', '  ', '<>', '¥%', '??', '()', '::',r'\/'
        ]
if len(argv) < 3:
    print(f'格式: {argv[0]} <图片> <文本>')
    exit()
img = Image.open(argv[1])
img = img.convert('L')
img.thumbnail((70,img.size[1]))
arr = np.array(img)
arr = ((arr+1)/16).tolist()
length = range(len(arr))
for i1 in length:
    for i2 in range(len(arr[i1])):
        arr[i1][i2] = string[int('{:.0f}'.format(arr[i1][i2]))-1]
for i in length:
    arr[i] = ''.join(arr[i])+'\n'
with open(argv[2],'w') as f:
    f.writelines(arr)
