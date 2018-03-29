#!/usr/bin/env python
#coding:utf-8

from ConfigParser import ConfigParser
import redis
from logger import logger
from elasticsearch import Elasticsearch
import sys
Config_file='config'

class Config(object):
    def __init__(self,config=Config_file):
        self.file = config
        self.con = self.parser()
    def parser(self):
        cf = ConfigParser()
        cf.read(self.file)
        return cf



def Redis():
    cf = Config()
    try:
        host = cf.con.get('redis','host')
        port = cf.con.get('redis','port')
        password = cf.con.get('redis','password')
	if not password:
        	return  redis.Redis(host=host,port=int(port))
	else:
		return redis.Redis(host=host,port=int(port),password=password)
    except Exception,e:
        logger('config redis get: %s' %(str(e)))
        sys.exit(10)

def es():
    cf = Config()
    try:
        host = cf.con.get('elasticsearch','host')
        port = cf.con.get('elasticsearch','port')
        return  Elasticsearch(host=host,port=port) 
    except Exception,e:
        logger('config elasticsearch get: %s' %(str(e)))
        sys.exit(10)
