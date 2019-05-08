import scrapy
from law.items import ContentItem
import urllib
import json

class ContentsSpider(scrapy.Spider):
    name = "contents"

    def start_requests(self):
        urls = []
        with open('urls.json', 'rb') as file :
            objects = json.load(file)
            for ob in objects :
                urls.append(ob['url'])

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # chapters = [i.strip() for i in response.css('.law-content .char-2::text').extract()]
        content = [i.strip() for i in response.css('.law-reg-content *::text').extract() if i.strip() != '']
        item = ContentItem()
        item['title'] = response.css('#hlLawName::text').extract_first(default="Missing")
        item['url'] = response.url
        item['time'] = response.css('#trLNNDate td::text').extract_first(default="Missing").strip()
        item['content'] = content

        return item