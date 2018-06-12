# -*- coding: utf-8 -*-

import time

import pymysql

from SpiderHunHun520 import settings


class Spiderhunhun520_chapterInfo_Pipeline(object):

    def __init__(self):
        '''初始化连接数据库'''

        print("正在为写入章节信息连接数据库")

        time.sleep(5)

        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

        print("数据库连接成功")


    def process_item(self, item, spider):


        try:

            self.cursor.execute(
                "insert into chapter_info (chapter_id,chapter_name,chapter_link,chapter_content,chapter_related_to_novel) "
                "values(%s,%s,%s,%s,%s)",
                [item['chapter_id'], item['chapter_name'], item['chapter_link'],
                 item['chapter_content'],  item['chapter_related_to_novel']])

            # 提交sql语句
            self.connect.commit()

            print("章节信息:%s,写入数据库成功" % item['chapter_name'])

        except Exception as error:

            with open("chapter.log", "a+") as f:

                f.write(time.strftime("%Y-%m-%d %H:%M:%S  ")+"Exception: 章节信息:%s,写入失败" % item['chapter_name']+"   原因:%s"%error+"\n")

            print("章节信息:%s,写入失败:%s"%(item['chapter_name'],error))

        return item
