#!/usr/bin/env python
#coding:utf-8

import time
import getpass

def logger(msg):
    with open('running.log','a+') as file:
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        user = getpass.getuser()
        file.write("%s \t %s: %s\n" %(datetime,user,msg))

def outer(msg):
    logger(msg)
    print msg
