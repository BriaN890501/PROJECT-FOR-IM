# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlItem(scrapy.Item):
    # define the fields for your item here like:
	title = scrapy.Field()
	url = scrapy.Field()

class ContentItem(scrapy.Item):
    # define the fields for your item here like:
	title = scrapy.Field()
	url = scrapy.Field()
	time = scrapy.Field()
	content = scrapy.Field()