
dirScan是python3 多进程版本目录扫描探测，支持http和socket代理隐藏自己真实IP，支持手动设置UA，COOKIE的headers,支持自定义success_status_code,内置php，asp，dir，jsp，mdb等常规目录探测，也可以自己添加目录

### 作者信息：

    author: jeffery.yu
    blog:  www.yu2lulu.xyz
    dependent_on:  requests/multiprocessing/configparser/re/random
    
### 使用方法:
    Usage: dirscan.py [options]
    Options:
      -h, --help            show this help message and exit
      -u URL, --url=URL     【必选】设置目标url信息
      -p POFNUM, --process=POFNUM
                            设置进程数,默认为4
      -d DICT, --dictory=DICT
                            【必选】设置dict目录下的遍历字典

      Example:  
                 python dirscan.py  -p 4 -u http://127.0.0.1  -d
        [ASP.txt|ASPX.txt|DIR.txt|JSP.txt|MDB.txt|PHP.txt]


### 目录结构：
    config/
        config.ini
    dict
        ASP.txt
        ASPX.txt
        DIR.txt
        JSP.txt
        MDB.txt
        PHP.txt
    dirscan.py
    readme
    result.txt






