from os import popen
from sys import argv
from json import load
from time import sleep

with open('font.py') as tmp:
    font = load(tmp)

def large_print(con):
    base = ''
    for i1 in range(6):
        for i2 in con:
            base += font[i2][i1]
        base += '\n'
    print(base,end='')

for i in range(100):
    large_print(str(i).rjust(3,str(0)))
    sleep(0.1)
    print('\033[6A\033[10D',end='')
