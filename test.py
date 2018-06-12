# -*- coding: utf-8 -*-

import re
from urllib.parse import quote
from time import sleep

import requests

class hunhun520:

    def __init__(self):

        self.visit_url=[]

        self.novelName=''

        self.spiderUrl=[]

        self.novelLink=[]

    def get_novel_pages(self):

        self.novelName=input("请输入小说:")

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

            with open('搜索{}的小说结果.txt'.format(self.novelName),'a',encoding='utf8') as f:

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

                    with open('搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

                        f.write("小说类型:{},链接:{},名称:{},最新一章:{},作者:{},最后更新时间:{}".format(novel_type,novel_link,novel_name,novel_last_chapter,novel_author,novel_last_pubdate)+"\n")

                        f.close()

            except requests.exceptions.ConnectTimeout as e1:

                print("访问第{}页失败:ConnectTimeout".format(pageNum + 1) + "\n")

                with open('搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

                    f.write("访问第{}页失败:ConnectTimeout".format(pageNum+1)+"\n")

                    continue

            except requests.exceptions.ConnectionError as e2:

                print("访问第{}页失败:ConnectionError".format(pageNum + 1) + "\n")

                with open('搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

                    f.write("访问第{}页失败:ConnectionError".format(pageNum + 1) + "\n")

                    continue

            except requests.exceptions.ReadTimeout as e3:

                print("访问第{}页失败:ReadTimeout".format(pageNum + 1) + "\n")

                with open('搜索{}的小说结果.txt'.format(self.novelName), 'a', encoding='utf8') as f:

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

if __name__ == '__main__':

    Spider=hunhun520()

    try:

        Spider.get_novel_pages()

        print("已获取所有页面链接")

        Spider.get_novel_info()

        Spider.get_spiderUrl()

    except requests.exceptions.ConnectionError as e1:

        print("网络出错,请检查网络连接状况")





