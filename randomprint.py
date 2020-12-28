from os import popen
from time import sleep
from random import randint

def get_xy():
    size = popen('stty size').read()
    size = size.split(' ')
    size[0],size[1] = int(size[0]),int(size[1])
    return size[0],size[1]

size = get_xy()
print('\033[s\033[2J',end='')

for i in range(100):
    x,y = randint(0,size[0]),randint(0,size[1])
    c,b = randint(30,39),randint(40,49)
    print(f'\033[{c};{b}m\033[{x};{y}H[]',end='',flush=True)
    sleep(0.05)
print('\033[0m\033[u',end='')
