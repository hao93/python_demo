#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

url = 'https://unsplash.com/napi/feeds/home'
headers = {'Authorization':'Client-ID c94869b36aa272dd62dfaeefed769d4115fb3189a9d1ec88ed457207747be626'}
proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
# index = 0

def home(nextPage, index):
    res = requests.get(nextPage, headers=headers, proxies=proxies).text
    msg = json.loads(res)
    photos = msg['photos']
    for pic in photos:
        downloadPic(pic['urls']['full'], pic['id'], index)
        index = index + 1
    return home(msg['next_page'], index+1)

def downloadPic(picUrl, picName, index):
    try:
        print('开始下载 第' + str(index))
        html = requests.get(picUrl, proxies=proxies)
        with open('pic/' + picName + '.jpg', 'wb') as file:
            file.write(html.content)
        print('下载结束 第' + str(index))
    finally:
        print('\n')

if __name__ == '__main__':
    home(url, 1)