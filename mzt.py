# coding:utf-8
import requests
from lxml import html
import os,threading,time
from tqdm import *

url = 'http://www.mzitu.com/page/{page}'

# 获取主页列表
def getPage(pagenum):
    baseUrl = url.format(page=pagenum)
    selector = html.fromstring(requests.get(baseUrl).content)

    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        print(i)
        urls.append(i)
    return urls

# 图片链接列表，标题
# url是详情页链接
def getPiclink(url):
    print(url)
    sel = html.fromstring(requests.get(url).content)
    # 图片总数 倒数第二项里
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]
    # 接下来的链接放到这个列表
    jpgList = []
    desc = u'获取图片链接：%s' % (title)
    print(desc)
    for i in range(int(total)):
        try:
            headers = {'Referer':'http://www.mzitu.com/99566/2'}
            # 每一页
            link = '{}/{}'.format(url, i+1)
            s = html.fromstring(requests.get(link, headers=headers).content)
            # 图片地址在src标签中
            jpg = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            # 图片链接放进列表
            jpgList.append(jpg)
        except:
            print('error download ...')
    return [title, jpgList]

# 下载图片
# 因为上面函数返回的两个值，这里我们直接传入一个两个值tuple
def downloadPic(title, piclist):
    print('----------------->')
    k = 1
    # 图片数量
    count = len(piclist)
    # 文件夹格式
    dirName = u"【%sP】%s" % (str(count), title)
    dirName.replace(' ', '')
    # 新建文件夹
    os.mkdir('pic/' + dirName)
    # print u'开始下载图片:%s 共%s张' % (dirName, len(piclist))
    desc = u'开始下载图片:%s 共%s张' % (dirName, len(piclist))
    # print desc
    headers = {'Referer':'http://www.mzitu.com/99566/2'}
    # print '\n'
    for i in piclist:
        # 文件写入的名称：当前路径／文件夹／文件名
        filename = '%s/pic/%s/%s.jpg' % (os.path.abspath('.'), dirName, k)
        print(u'开始下载图片:%s 第%s张' % (dirName, k))

        with open(filename, "wb") as jpg:
            jpg.write(requests.get(i, headers=headers).content)
        k += 1

        # coding:utf-8


if __name__ == '__main__':
    # task_pool=threadpool.ThreadPool(8)#8是线程池中线程的个数
    for i in range(1, 1000):
        threads = []
        for link in getPage(i):
            try:
                queue_list = []
                jpgList = getPiclink(link)
                # downloadPic(jpgList[0], jpgList[1])
                t = threading.Thread(target=downloadPic, name=jpgList[0], args=(jpgList[0],jpgList[1]))
                threads.append(t)
                # queue_list.append(threadpool.makeRequests(downloadPic, jpgList))
                # map(task_pool.putRequest,queue_list)
                t.start()
            except:
                a = 1
    t.join()
    time.sleep(10000)
    # task_pool.poll()