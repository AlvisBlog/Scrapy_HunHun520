# -*- coding: utf-8 -*-

import pymysql
import os


novel_name=input("请输入小说名称:")

try:
    print("连接数据库中")

    db=pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='',
        charset='utf8',
        database='hunhun520'
    )

    print('数据库连接成功')

    cursor = db.cursor()

    sql = "SELECT chapter_name,chapter_content FROM chapter_info WHERE chapter_related_to_novel='{}' ORDER BY chapter_id".format(novel_name)

    cursor.execute(sql)

    result = cursor.fetchall()

    try:

        os.mkdir('novel')

    except Exception as e:

        pass

    print("开始写入章节信息")

    for data in result:

        with open('./novel/{}.txt'.format(novel_name), 'a+', encoding='utf8') as f:

            f.write(data[0] + "\n")

        try:
            chapter_content = data[1].split('　　')

            for content in chapter_content:

                with open('./novel/{}.txt'.format(novel_name), 'a+', encoding='utf8') as f:

                    f.write(content + '\n')

            with open('./novel/{}.txt'.format(novel_name), 'a+', encoding='utf8') as f:

                f.write('\n' + '\n' + '\n')

        except Exception as e:

            print("章节信息:%s,写入失败:%s"%(e,data[1]))

        print(data[0])

except Exception as e:

    print('数据库连接失败:%s'%e)













