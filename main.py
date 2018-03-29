#!/usr/bin/env python
#coding:utf-8

from service import Redis, es
from logger import logger
import sys
s_file = "status.log"

D_value = {'indices':{'indexing':["index_total","delete_current"],"search":["query_total"],"merges":["total_docs"]}}
C_value = {'indices':{"indexing":['index_current'],"search":["open_contexts"],"merges":["current_docs"],"query_cache":["hit_count","miss_count"],'segments':["count"],'request_cache':['hit_count','miss_count']},'jvm':{"mem":["heap_used_percent"],"threads":["count"],"gc":["collectors.young.collection_count","collectors.young.collection_time_in_millis","collectors.old.collection_count","collectors.old.collection_time_in_millis"]},"process":{"open_file_descriptors":[]}}

f = open(s_file,'w')
f.close()
f = open(s_file,'w+')
def start():
    array_node = {'D-value':{'value':D_value,'flag': 0},'C_value':{'value':C_value,'flag': 1}}
    #array_node = {'D-value':{'value':D_value,'flag': 0}}
    get_nodes_value(array_node)
    get_cluster_value()
    f.close()   
                    

def get_nodes_value(array_node):
    Es = es()
    nodes_data = Es.nodes.stats()['nodes']
    Re = Redis()
    nodes_key = nodes_data.keys()
    for res in array_node:
        A_value = array_node[res]['value']
        flag = array_node[res]['flag']
	for key in nodes_key:
            node_name = nodes_data[key]['name']
            for indices in A_value.keys():
                for field in A_value[indices]:
                    field_data = A_value[indices][field]
                    length = len(field_data)
                    for i in range(length):
                        itemdata = field_data[i]
                        item_list = itemdata.split('.')
                        item_length = len(item_list)
                        value = nodes_data[key][indices][field]
                        for k in range(item_length):
                            value = value['%s' %(item_list[k])]
                        redis_key = node_name + '.'+ indices + '.' + field + '.' + itemdata
                        try:
                            if flag == 0:
                                old_value = Re.get(redis_key)
                                if not old_value:
                                    old_value = 0
                                count = int(value) - int(old_value)
                                f.write('%s %s\n' %(redis_key,str(count)))
                            elif flag == 1:
                                f.write('%s %s\n' %(redis_key,str(value))) 
                            Re.set(redis_key,value)
                        except Exception,e:
                            logger('%s inserting into redis is  failed,due to: %s\n' %(redis_key,str(e)))
		    if length == 0:
			value = nodes_data[key][indices][field]
			redis_key = node_name + '.'+ indices + '.' + field
			Re.set(redis_key,value)
			f.write('%s %s\n' %(redis_key,str(value)))

def get_cluster_value():
    Es = es()
    Re = Redis()
    cluster_data = Es.cluster.health(level='indices')
    status = cluster_data['status']
    f.write('%s %s\n' %('cluster.status',status))
    Re.set('cluster.status',status) 
    if status != "green":
        for key in cluster_data['indices'].keys():
            if cluster_data['indices'][key]['status'] != "green":
                f.write('%s %s\n' %('cluster.status.error_indices',cluster_data['indices'][key]['status']))


if __name__ == "__main__":
    start()  

