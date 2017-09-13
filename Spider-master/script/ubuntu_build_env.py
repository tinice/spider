# -*- coding: utf-8 -*-
from fabric.api import *
env.hosts = ['poluo@123.207.124.212:22',]

# env.password = 'test'
#-------------安装python3.4-----------------
def install_python3():
    sudo('apt-get install epel-release')
    sudo('apt-get install python34')
    sudo('curl -O https://bootstrap.pypa.io/get-pip.py')
    sudo('/usr/bin/python3.4 get-pip.py')
    sudo('apt-get install python34-devel')

#------------配置cryptography---------------
def config_cryptography():
    sudo('apt-get install gcc libffi-devel python-devel openssl-devel')

#------------安装iftop----------------------
def install_iftop():
    sudo('apt-get install iftop')
#------------安装、配置virtualenv----------------
def install_virtualenv():
    sudo('pip install virtualenv')
    run('virtualenv test --python=/usr/bin/python3')

#------------安装scrapy、requests、pymongo----------
def install_scrapy():
    with cd('./test'):
        with prefix('source ./bin/activate'):
            run('pip install scrapy')
            run('pip install requests')
            run('pip install pymongo')

#------------上传文件------------------------------
def upload_file():
    pass
#-----------执行指定的任务-----------------
def task():
    #install_iftop()
    #install_python3()
    #config_cryptography()
    install_virtualenv() 
    install_scrapy()  
