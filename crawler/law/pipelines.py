# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

class LawPipeline(object):
    items = []

    def close_spider(self, spider):
        origin = []
        if(os.path.isfile(spider.name+'.json')):
            with open(spider.name+'.json', 'r') as file:
                origin = json.load(file)
        origin.extend(self.items)
        with open(spider.name+'.json', 'w') as file:
            json.dump(origin, file)

    def process_item(self, item, spider):
        self.items.append(dict(item))

        return item