main.py：用户每分钟更新一次es集群的全部数据
discovery.py：将main.py更新的数据转化为zabbix 自动检测的数据

在zabbix配置中加入这两个：
UserParameter=check.es.discovery,/usr/local/monitor/elasticsearch/discovery.py
UserParameter=es.check[*],cat /usr/local/monitor/elasticsearch/status.log |grep $1|grep $2|awk '{print $NF}'

然后在zabbix的自动发现中自动发现规则（check.es.discovery），再增加监控项(es.check[*])
如果遇见问题，请留言
