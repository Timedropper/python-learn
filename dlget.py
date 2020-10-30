#!/data/data/com.termux/files/usr/bin/python
from sys import argv
from mymoudle import threads_downloader
header = {
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 10; PCT-AL10 Build/HUAWEIPCT-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36'}
if len(argv) == 3:
    thread = 8
elif len(argv) == 4:
    thread = int(argv[3])
else:
    print(f'格式: {argv[0]} <链接> <路径> <线程(可选)>')
    exit()
threads_downloader(argv[1],argv[2],header,thread)
