from time import sleep
from random import shuffle
from os import listdir,popen

Music = listdir('/sdcard/Music/rewind/netease/')
shuffle(Music)

def get_status():
    info = []
    status = popen('termux-media-player info').read()
    if status == 'No track currently!\n':
        info.append(False)
    else:
        info.append(True)
        info.append(status[-14:-1])
    return info

def play(path):
    popen(f"termux-media-player play '/sdcard/Music/rewind/netease/{path}'")

try:
    for i in Music:
        play(i)
        status = get_status()
        while status[0]:
            print(i,status[1].replace('.mp3',''),end='\r')
            sleep(0.9)
            status = get_status()
except:
    popen('termux-media-player stop')
    print()
