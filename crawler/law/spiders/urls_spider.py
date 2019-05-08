import scrapy
from law.items import UrlItem
import urllib

class UrlsSpider(scrapy.Spider):
    name = "urls"

    def start_requests(self):
        keywords = ['信用合作社法', '銀行法']
        urls = []
        for keyword in keywords:
            urls.append('https://law.moj.gov.tw/Law/LawSearchResult.aspx?ty=ONEBAR&kw='+urllib.parse.quote_plus(keyword))


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        link = 'https://law.moj.gov.tw/'
        title = urllib.parse.unquote(response.url[response.url.find('kw=')+3:])
        suburl = response.css('a[title="'+title+'"]::attr(href)').extract_first(default='Missing')
        item = UrlItem()
        item['title'] = title
        item['url'] = link+suburl[suburl.find('../')+3:]

        return item