from tqdm import tqdm
from json import loads,dumps
from requests import session
from qrcode.console_scripts import main as draw

Session = session()

def bangumi(url):
    global Session
    base_url = 'http://api.bilibili.com/pgc/view/web/season?'
    if 'ep' in url:
        url = base_url + 'ep_id=' + url.split('ep')[-1]
    else:
        url = base_url + 'season_id=' + url.split('ss')[-1]
    descri = loads(Session.get(url).text)
    bvid = descri['result']['episodes'][0]['bvid'].split('BV')[-1]
    cid = descri['result']['episodes'][0]['cid']
    ep_id = descri['result']['episodes'][0]['id']
    url = f'https://api.bilibili.com/pgc/player/web/playurl?bvid={bvid}&cid={cid}&qn=80&type=&otype=json&ep_id={ep_id}&fnver=0&fnval=16'
    content = loads(Session.get(url).text)
    return (content,descri)

def missionpool(target,args,moudle=0,joins=False):
    if moudle == 0:
        if not 'Thread' in dir():
            from threading import Thread as mission
    elif moudle == 1:
        if not 'Process' in dir():
            from multiprocessing import Process as mission
    pool = []
    if type(args) == int:
        for i in range(args):
            pool.append(mission(target=target))
    else:
        for i in args:
            pool.append(mission(target=target,args=i))
    for i in pool:
        i.start()
    if joins:
        for i in pool:
            i.join()
    return pool

def  BiliCookie():
    global Session
    login = loads(Session.get('http://passport.bilibili.com/qrcode/getLoginUrl').content)
    draw([login['data']['url']])
    input('等待扫描二维码')
    data = {'oauthKey':login['data']['oauthKey']}
    Session.post('http://passport.bilibili.com/qrcode/getLoginInfo',data=data)
    files = open('cookie.txt','w')
    files.write(dumps(Session.cookies.get_dict(),indent=2,separators=(',',':'),ensure_ascii=False,sort_keys=True))

def single_downloader(url,path):
    global Session
    files = open(path,'wb')
    source = Session.get(url,stream=True)
    if 'Content-Length' in source.headers:
        total = int(source.headers['Content-Length'])
    else:
        total = 0
    progress = tqdm(total=total,unit='iB',unit_scale=True)
    for i in source.iter_content(8192):
        files.write(i)
        progress.update(len(i))
    files.close()

def int_split(size,url,path,chunks):
    if size % chunks == 0:
        start = [i for i in range(0,size,int(size / chunks))]
        tmp_int = size / chunks - 1
        stop = [i + tmp_int for i in start]
    else:
        start = [i for i in range(0,size,size // chunks + 1)]
        tmp_int = size // chunks
        stop = [i + tmp_int for i in start]
        stop[-1] = size - 1
    return [(i1,int(i2),url,path) for i1,i2 in zip(start,stop)]

def threads_downloader(url,path,threads=8):
    global Session
    global progress
    progress = tqdm(unit='iB',unit_scale=True)
    open(path,'w').close()
    source = Session.get(url,stream=True)
    total_size = int(source.headers['Content-Length'])
    chunk = int_split(total_size,url,path,threads)
    missionpool(downloader,args=chunk,moudle=1)

def downloader(Range1,Range2,url,path):
    global Session
    global progress
    Session.headers.update({'Range':f'bytes={Range1}-{Range2}'})
    source = Session.get(url,stream=True)
    files = open(path,'rb+')
    files.seek(Range1)
    for chunk in source.iter_content(8192):
        files.write(chunk)
        progress.update(len(chunk))

def get_splash():
    global Session
    ts = 0
    appkey = '1d8b6e7d45233436'
    sign = '78a89e153cd6231a4a4d55013aa063ce'
    url = f'http://app.bilibili.com/x/v2/splash/brand/list?appkey={appkey}&ts={ts}&sign={sign}'
    content = loads(Session.get(url).content)['data']['list']
    return content

Url = 'https://b23.tv/ep330484'
Headers = {
        'User-Agent':
        'Bilibili Freedoooooom/MarkII',
        'Referer':'https://search.bilibili.com'
        }
Session.headers.update(Headers)
cookie = loads(open('cookie.txt').read())
Session.cookies.update(cookie)
