# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spiderhunhun520_novelInfo_Item(scrapy.Item):

    novel_name = scrapy.Field()

    novel_author = scrapy.Field()

    novel_type = scrapy.Field()

    novel_link = scrapy.Field()

    novel_introduce = scrapy.Field()

class Spiderhunhun520_chapterInfo_Item(scrapy.Item):

    chapter_link = scrapy.Field()

    chapter_id = scrapy.Field()

    chapter_name = scrapy.Field()

    chapter_related_to_novel=scrapy.Field()

    chapter_content=scrapy.Field()

