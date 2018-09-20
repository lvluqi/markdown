<center>sentrylogs<center>
---
>**简介**
```
sentrylogs是python开发，使用raven进行收集nginxerror日志并发送到sentry的工具
```
>**安装**
```
pip install sentrylogs
```
>修改sentrylogs运行python版本
```
在你所安装的python根目录下找到 .lib/python3.5/site-packages/sentrylogs
$ tree
.
├── bin
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-35.pyc
│   │   └── sentrylogs.cpython-35.pyc
│   └── sentrylogs.py	#运行命令
├── conf
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-35.pyc
│   │   └── settings.cpython-35.pyc
│   └── settings.py   #配置文件
├── daemonize.py   #守护进程程序
├── helpers.py      
├── __init__.py
├── parsers     #解析目录
│   ├── __init__.py
│   ├── nginx.py   #解析nginx error日志
│   └── __pycache__
│       ├── __init__.cpython-35.pyc
│       └── nginx.cpython-35.pyc
└── __pycache__
    ├── daemonize.cpython-35.pyc
    ├── helpers.cpython-35.pyc
    └── __init__.cpython-35.pyc

$ vim sentrylogs.py
修改#!/bin/env/python > #!/bin/env/python3
```
>sentrylogs命令帮助
```
$ sentrylogs
usage: sentrylogs [-h] [--sentryconfig SENTRYCONFIG] [--sentrydsn SENTRYDSN]
                  [--daemonize] [--follow FOLLOW]
                  [--nginxerrorpath NGINXERRORPATH]

Send logs to Django Sentry.

optional arguments:
  -h, --help            show this help message and exit
  --sentryconfig SENTRYCONFIG, -c SENTRYCONFIG
                        A configuration file (.ini, .yaml) of some Sentry
                        integration to extract the Sentry DSN from
  --sentrydsn SENTRYDSN, -s SENTRYDSN
                        The Sentry DSN string (overrides -c)
  --daemonize, -d       Run this script in background
  --follow FOLLOW, -f FOLLOW
                        Which logs to follow, default ALL
  --nginxerrorpath NGINXERRORPATH, -n NGINXERRORPATH
                        Nginx error log path
```
>DSN获取方式
```
sentry >> project >> setting >> client DSN 查看
```
