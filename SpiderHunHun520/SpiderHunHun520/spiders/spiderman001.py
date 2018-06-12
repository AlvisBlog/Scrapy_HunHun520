# -*- coding: utf-8 -*-

import re
import os
from urllib.parse import quote
from time import sleep

import scrapy
import requests

from SpiderHunHun520.items import Spiderhunhun520_novelInfo_Item,Spiderhunhun520_chapterInfo_Item




class hunhun520:
    '''获取爬取目标URL'''

    def __init__(self):

        self.visit_url=[]

        self.novelName=''

        self.spiderUrl=[]

        self.novelLink=[]

        try:
            os.mkdir('SearchResult')
        except Exception as e:
            pass

    def get_novel_pages(self):

        self.novelName=input("请输入小说(多于一个字):")

        #decodeUrl
        searchKey=quote(self.novelName,encoding='gbk')

        #形成第一条获取页面信息Url
        firstUrl='https://www.hunhun520.com/novel.php?action=search&searchkey={}'.format(searchKey)

        #获取返回状态
        response=requests.post(firstUrl)

        #页面源代码
        html=response.text

        #最大页数
        maxPage=int(re.findall('页/(.*?)页',html,re.S)[0])

        #获取每个页面访问的token参数
        token_url=re.findall('<div class="page">.*?<a href="(.*?)&page=1"',html,re.S)[0]

        #每个页面的链接
        for page in range(1,maxPage+1):

            self.visit_url.append(token_url+"&page={}".format(page))

        return self.visit_url

    def get_novel_info(self):

        for pageNum in range(len(self.visit_url)):

            sleep(3)

            print("正在访问第{}页".format(pageNum+1))

            with open('./SearchResult/搜索{}的小说结果.txt'.format(self.novelName),'a',encoding='utf8') as f:

                f.write("正在访问第{}页".format(pageNum+1)+"\n")

                f.close()

            try:

                html=requests.get(self.visit_url[pageNum],timeout=3).text

                novel_data=re.findall('<ul>(.*?)</ul>',html,re.S)[1]

                novel_list=re.findall('<li>(.*?)</li>',novel_data,re.S)

                for novel in novel_list:

                    novel_type=re.findall('<span class="s1">(.*?)</span>',novel,re.S)[0].replace('[','').replace(']','')

                    novel_link=re.findall('<span class="s2"><a href="(.*?)"',novel,re.S)[0]

                    novel_name=re.findall('<span class="s2">.*?>(.*?)<',novel,re.S)[0]

                    novel_last_chapter=re.findall('<span class="s3">.*?>(.*?)<',novel,re.S)[0]

                    novel_author=re.findall('<span class="s4">(.*?)<',novel,re.S)[0]

                    novel_last_pubdate=re.findall('<span class="s5">(.*?)</span>',novel,re.S)[0]

                    self.novelLink.append(novel_link)

                    print("小说类型:{},链接:{},名称:{},最新一章:{},作者:{},最后更新时间:{}".format(novel_type,novel_link,novel_name,novel_last_chapter,novel_author,novel_last_pubdate))

                    print()

                    with open('./SearchResult/搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

                        f.write("小说类型:{},链接:{},名称:{},最新一章:{},作者:{},最后更新时间:{}".format(novel_type,novel_link,novel_name,novel_last_chapter,novel_author,novel_last_pubdate)+"\n")

                        f.close()

            except requests.exceptions.ConnectTimeout as e1:

                print("./SearchResult/访问第{}页失败:ConnectTimeout".format(pageNum + 1) + "\n")

                with open('搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

                    f.write("访问第{}页失败:ConnectTimeout".format(pageNum+1)+"\n")

                    continue

            except requests.exceptions.ConnectionError as e2:

                print("访问第{}页失败:ConnectionError".format(pageNum + 1) + "\n")

                with open('./SearchResult/搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

                    f.write("访问第{}页失败:ConnectionError".format(pageNum + 1) + "\n")

                    continue

            except requests.exceptions.ReadTimeout as e3:

                print("访问第{}页失败:ReadTimeout".format(pageNum + 1) + "\n")

                with open('./SearchResult/搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

                    f.write("访问第{}页失败:ReadTimeout".format(pageNum + 1) + "\n")

                    continue

    def get_spiderUrl(self):

        choose=input("请输入想要爬取的Url:")

        if choose=='q':

            print("退出爬虫")

        elif choose=='all':

            print("你选择爬取全部链接")

            self.spiderUrl=self.novelLink

            print("以下是你所需要爬取的Url列表,总共有{}条".format(len(self.spiderUrl)))

            for url in self.spiderUrl:

                print(url)

        else:

            chooseUrl=choose.split(',')

            for url in chooseUrl:

                if url in self.novelLink:

                    self.spiderUrl.append(url)

            if self.spiderUrl==[]:

                print("你的选择为空")

            else:

                print("以下是你所需要爬取的Url列表,总共有{}条".format(len(self.spiderUrl)))

                for url in self.spiderUrl:

                    print(url)

        return self.spiderUrl


class Spiderman001Spider(scrapy.Spider):
    Spider = hunhun520()

    try:

        Spider.get_novel_pages()

        print("已获取所有页面链接")

        Spider.get_novel_info()

        start_urls =Spider.get_spiderUrl()

    except requests.exceptions.ConnectionError as e1:

        print("网络出错,请检查网络连接状况")

    except IndexError as e2:
        print("搜索字段太短")

    name = 'spiderman001'


    def parse(self, response):

        novelItem=Spiderhunhun520_novelInfo_Item()

        html = response.text

        novelInfo=re.findall('<div id="info">(.*?)</div>',html,re.S)[0]

        #小说名称
        novelItem['novel_name'] =re.findall('<h1>(.*?)</h1>',novelInfo,re.S)[0]

        #小说作者
        novelItem['novel_author'] =re.findall('<p>.*?：(.*?)</p>',novelInfo,re.S)[0]

        #小说类型
        novelItem['novel_type'] =re.findall('<p>.*?：(.*?)</p>',novelInfo,re.S)[1]

        #小说链接
        novelItem['novel_link'] = response.url

        #简介数据
        introduce_data=re.findall('<div id="intro">.*?</p>(.*?)</div>',html,re.S)[0].strip().replace('&nbsp;','').replace('&hellip;','').replace('<br />','')

        #简介提取数据
        introduce=re.findall('<p>(.*?)</p>',introduce_data,re.S)

        novelItem['novel_introduce']=''

        for data in introduce:

            novelItem['novel_introduce']=data+novelItem['novel_introduce']


        yield novelItem

        chapter=re.findall('<dl>(.*?)</dl>',html,re.S)[0]

        chapterUrl=re.findall('<dd><a href="(.*?)"',chapter,re.S)

        for url in chapterUrl:

            yield scrapy.Request(url=url,meta={'novel_name':novelItem['novel_name']},callback=self.parse_chapter)

    def parse_chapter(self,response):

        chapterItem = Spiderhunhun520_chapterInfo_Item()

        html=response.text

        #章节链接
        chapterItem['chapter_link']=response.url

        #章节ID
        chapterItem['chapter_id'] =re.findall('https://www.hunhun520.com/book/.*?/(.*?).html',chapterItem['chapter_link'],re.S)[0]

        #章节名称
        chapterItem['chapter_name']=re.findall('<h1>(.*?)</h1>',html,re.S)[0]

        #关联小说
        chapterItem['chapter_related_to_novel']=response.meta['novel_name']

        #第一页章节内容
        First_chapter_content =re.findall('<div id="txtright">.*?</div>(.*?)<!--over-->',html,re.S)[0].strip().replace('<br /><br />','')

        try:
            # 第二页章节链接

            NextUrl = 'https://www.hunhun520.com/book/'+re.findall('https://www.hunhun520.com/book/(.*?)/',response.url,re.S)[0]+'/{}_2.html'.format(chapterItem['chapter_id'])

            # 第二页章节源码
            NextHtml = requests.get(NextUrl).text

            #第二页章节内容
            Next_chapter_content=re.findall('<div id="txtright">.*?</div>(.*?)<!--over-->',NextHtml,re.S)[0].strip().replace('<br />','')

            #章节内容
            chapterItem['chapter_content']=First_chapter_content+Next_chapter_content

        except Exception as e1:

            # 章节内容
            chapterItem['chapter_content'] = First_chapter_content

        print('章节信息:{}已获取'.format(chapterItem['chapter_name']))

        yield chapterItem











