#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import threading,os
from elasticsearch import Elasticsearch
import elasticsearch.helpers
import time


baseURL = 'http://www.cnbeta.com/home/more?type=all&page={page}'
headers = {'Referer' : 'http://www.cnbeta.com/'}
index = 0



def getRes(page):
    global index
    actions=[]
    print('开始爬取第 %d 页, 共爬去新闻 %d 条' % (page, index))
    url = baseURL.format(page = page)
    res = requests.get(url, headers = headers).text
    msg = json.loads(res)
    result = msg['result']['list']

    for i in result:
        i['inputtime'] = i['inputtime'] + ':00',
        action = {
            "_id": i['sid'],
            "_source": i
        }
        actions.append(action)
        index = index + 1
    insertEs(actions)

def insertEs(actions):
    # es client, by default connect to localhost:9200
    es = Elasticsearch()
    elasticsearch.helpers.bulk(es, actions, index='cnbeta', doc_type='all', )
    # print('插入es： %d' % len(actions))

def log(page, time):
    action = {
        "_id": page,
        "_source": {
            "time": time,
            "page": page
        }
    }
    actions = []
    actions.append(action)
    es = Elasticsearch()
    elasticsearch.helpers.bulk(es, actions, index='logs', doc_type='cnbeta', )


if __name__ == '__main__':
    threads = []
    for i in range(1,10975):
        start = time.time()
        getRes(i)
        end = time.time()
        print('耗时 %s s' % (end - start))
        log(i, (end - start))
