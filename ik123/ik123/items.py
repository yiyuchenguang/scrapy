# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Ik123Item(scrapy.Item):
    image_paths = scrapy.Field()
    name = scrapy.Field()
    info = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()