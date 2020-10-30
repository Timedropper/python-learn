if not 'session' in dir():
    from requests import session
def factorial(num):
    if num == 0:
        return 1
    else:
        result = 1
        for i in range(1,num+1):
            result = result*i
        return result

def bangumi_json(url,Session=session(),close_bool=True):
    if not 'json' in dir():
        import json
    base_url = 'http://api.bilibili.com/pgc/view/web/season?'
    if 'ep' in url:
        url = base_url + 'ep_id=' + url.split('ep')[-1]
    else:
        url = base_url + 'season_id=' + url.split('ss')[-1]
    respon = json.loads(Session.get(url).text)
    if close_bool:
        Session.close()
    return respon

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

def int_split(size,url,path,Session,chunks):
    if size % chunks == 0:
        start = [i for i in range(0,size,int(size / chunks))]
        tmp_int = size / chunks - 1
        stop = [i + tmp_int for i in start]
    else:
        start = [i for i in range(0,size,size // chunks + 1)]
        tmp_int = size // chunks
        stop = [i + tmp_int for i in start]
        stop[-1] = size - 1
    return [(i1,int(i2),url,path,Session) for i1,i2 in zip(start,stop)]

def threads_downloader(url,path,header,threads):
    if not 'session' in dir():
        from requests import session
    if not 'argv' in dir():
        from sys import argv
    Session=session()
    open(path,'w').close()
    Session.headers.update(header)
    source = Session.get(url,stream=True)
    total_size = int(source.headers['Content-Length'])
    chunk = int_split(total_size,url,path,Session,threads)
    missionpool(downloader,args=chunk,moudle=1)

def downloader(Range1,Range2,url,path,Session):
    Session.headers.update({'Range':f'bytes={Range1}-{Range2}'})
    source = Session.get(url,stream=True)
    files = open(path,'rb+')
    files.seek(Range1)
    for chunk in source.iter_content(8192):
        files.write(chunk)
