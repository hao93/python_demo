#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import threading,os
from elasticsearch import Elasticsearch
import elasticsearch.helpers

url = 'https://unsplash.com/napi/feeds/home'
headers = {'Authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}
proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
index = 0
done = 0

def home(nextPage):
    global index
    res = requests.get(nextPage, headers=headers).text
    msg = json.loads(res)
    photos = msg['photos']

    actions=[]
    threads = []
    for pic in photos:
        actions.append(pic)
        t = threading.Thread(target=downloadPic, name=index, args=(pic['urls']['full'], pic['id']))
        threads.append(t)
        index = index + 1
        t.start()
    insertEs(actions)
    print(index)
    t.join()
    return home(msg['next_page'])

def downloadPic(picUrl, picName):
    global done,index
    try:
        html = requests.get(picUrl)
        path = 'pic/' + picName + '.jpg'
        if os.path.exists(path):
            print(path, ' 已经存在')
        else:
            with open(path, 'wb') as file:
                file.write(html.content)

    finally:
        done = done + 1
        print(done,'/',index)

def insertEs(actions):
    # es client, by default connect to localhost:9200
    es = Elasticsearch()
    elasticsearch.helpers.bulk(es, actions, index='unsplash', doc_type='picdetail')

if __name__ == '__main__':
    home(url)