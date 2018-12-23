'''
author: jeffery.yu
blog:  www.yu2lulu.xyz
describe: a method to scan website
'''

import requests
from multiprocessing  import Process,Manager
import optparse
import configparser
import re
from random import choice

def readConfigini(section):
    config=configparser.ConfigParser()
    config.read("./config/config.ini")
    tmpdict={}
    for i in config[section]:
        tmpdict[i]=config[section][i]
    return tmpdict #{'Usar-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

def returnproxy():
    proxy=readConfigini('proxy')
    proxies=[]
    for k,v in proxy.items():
        if v=='None':
            proxies.append(None)
            break
        else:
            tmp={}
            tmp['http']=v
            tmp['https']=v
            proxies.append(tmp)
    return proxies  #[{'https': 'https://127.0.0.1', 'http': 'http://127.0.0.1'}, {'http': 'http://1.1.1.1', 'https': 'https://1.1.1.1'}]


def dirscan(url,dictQ,resultQ):
    while True:
        uri=dictQ.get()
        if uri=='bye':
            break
        headers=readConfigini('headers')
        success_status_code=readConfigini('success_status_code')['code'].split(',')
        proxy=choice(returnproxy())
        try:
            rep=requests.get(url=url+'/'+uri,headers=headers,proxies=proxy,timeout=1)
            if rep.status_code in success_status_code:
                print(url+uri,rep.status_code)
                resultQ.put(url+uri)
            else:
                pass
                print(url + uri, rep.status_code)
        except:
            pass

def main(url,pofnum,dict):
    #1.读取字典装载入程序
    dictQ=Manager().Queue()
    resultQ=Manager().Queue()
    ProcessList=[]

    for i in range(0,int(pofnum)):
        p=Process(target=dirscan,args=(url,dictQ,resultQ))
        ProcessList.append(p)
        p.start()

    with open("./dict/"+dict,encoding='gbk') as f:
        while True:
            uri=f.readline().strip()
            if uri!='':
                dictQ.put(uri)
            else:
                break
    for p in ProcessList:
        dictQ.put('bye')

    while True:
        if len(ProcessList)==0:
            break
        for p in ProcessList:
            if not p.is_alive():
                ProcessList.remove(p)


    #结果写入到本地文件中
    with open("result.txt", 'w') as f:
        for i in range(0,int(resultQ.qsize())):
            urldata=resultQ.get()+'\n'
            f.write(urldata)
    print("保存%s文件成功" %("result.txt"))

if __name__=="__main__":
    parse=optparse.OptionParser()
    parse.add_option("-u",'--url',dest='url',help='【必选】设置目标url信息')
    parse.add_option("-p",'--process',default=4,dest='pofnum',help='设置进程数,默认为4')
    parse.add_option("-d",'--dictory',dest='dict',help='【必选】设置dict目录下的遍历字典')
    example = optparse.OptionGroup(
        parse,
        'Example',
        '''
        python dirscan.py  -p 4 -u http://127.0.0.1  -d [ASP.txt|ASPX.txt|DIR.txt|JSP.txt|MDB.txt|PHP.txt]
        ''',
    )
    parse.add_option_group(example)
    (opts, argv) = parse.parse_args()
    if opts.url==None  or opts.dict==None:
        print("Usage: python dirscan.py  [-p 4] -u http://127.0.0.1 -d [ASP.txt|ASPX.txt|DIR.txt|JSP.txt|MDB.txt|PHP.txt]")
        exit()

    main(opts.url,opts.pofnum,opts.dict)