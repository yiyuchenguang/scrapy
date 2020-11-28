# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CPoemItem(scrapy.Item):
    poem_type = scrapy.Field()
    poem_url = scrapy.Field()
    poem_title = scrapy.Field()
    poem_author = scrapy.Field()
    poem_body = scrapy.Field()
    poem_yi = scrapy.Field()
    poem_zhu = scrapy.Field()
    poem_shang = scrapy.Field()




