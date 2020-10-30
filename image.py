#!/usr/bin/env python
from sys import argv
from numpy import array
from PIL.Image import open as img_open
str_line = [
        '[)', '<}', '€¥', '#1', '%V', 'l7', '**', '+=',
        '-+', '  ', '{>', '|%', '??', '(]', '::',r'\/'
        ]
def img_to_text(image,text):
    img = img_open(image)
    img = img.resize((190,88))
    img = img.convert('L')
    img = (array(img)//16).tolist()
    char = [''.join([str_line[i2] for i2 in i1]) + '\n' for i1 in img]
    with open(text,'w') as txt:
        txt.writelines(char)
img_to_text(argv[1],argv[2])
