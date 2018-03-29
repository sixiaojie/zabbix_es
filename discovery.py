#!/usr/bin/env python
#coding:utf-8
import os
s_file = "/usr/local/monitor/elasticsearch/status.log"
line_num = int(os.popen('wc -l %s' %(s_file)).read().split()[0]) - 1
count=int(os.popen('cat %s|grep green|wc -l' %(s_file)).read().split()[0])
if count == 1:
	line_num = int(os.popen('wc -l %s' %(s_file)).read().split()[0]) - 1
else:
	line_num = int(os.popen('wc -l %s' %(s_file)).read().split()[0]) -2
i = 0
print "{\n",
print "\t\"data\":["
f = open(s_file,'r')
####输出格式必须是json的格式，下面的{#HOST},{#ITEM}是zabbix_server上需要配置
for line in f.xreadlines():
	i = i + 1
	value = line.split()[1]
	line_data = line.split()[0]
	s_line = line_data.split('.')
	length = len(s_line)
	if length <=2:
		continue
	print "\t{"
	print "\t\t\"{#HOST}\":\"%s\"," %(s_line[0])
	print "\t\t\"{#ITEM}\":\"%s\"" %(".".join(s_line[1:]))
	#print "\t\t\"{#ITEM_VALUE}\":\"%s\"," %(value)
	if i < line_num:
		print "\t},",
	else:
		print "\t}",
print "\n\t]"
print "}"
