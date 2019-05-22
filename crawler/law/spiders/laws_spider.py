import scrapy
from law.items import ContentItem
import urllib
import json

class LawsSpider(scrapy.Spider):
    name = 'laws'
    link_ROC = 'https://law.moj.gov.tw/'
    link_Bank = 'https://law.banking.gov.tw/Chi/FLAW/'
    link_Inter = 'http://glrs.moi.gov.tw/'

    def start_requests(self):
        keywords = []
        with open('titles.json', 'rb') as file:
            keywords = json.load(file)
        # 全國法規資料庫
        urls_ROC = []
        # 金管會銀行局
        urls_Bank = []
        #內政部
        urls_Inter = []
        for keyword in keywords:
            kw = urllib.parse.quote_plus(keyword)
            urls_ROC.append('https://law.moj.gov.tw/Law/LawSearchResult.aspx?ty=ONEBAR&kw=' + kw)
            urls_Bank.append('https://law.banking.gov.tw/Chi/FLAW/FLAWQRY02.aspx?item=lname&pcode=all&type=a_all&cnt=15&kw=' + kw)
            urls_Inter.append('http://glrs.moi.gov.tw/LawResult.aspx?NLawTypeID=all&name=1&content=1&now=1&fei=1&size=100&kw=' + kw)

        for url in urls_ROC:
            yield scrapy.Request(url=url, callback=self.urls_ROC_parse)
        for url in urls_Bank:
            yield scrapy.Request(url=url, callback=self.urls_Bank_parse)
        for url in urls_Inter:
            yield scrapy.Request(url=url, callback=self.urls_Inter_parse)


    def urls_ROC_parse(self, response):
        title = urllib.parse.unquote(response.url[response.url.find('kw=')+3:])
        suburl = response.css('a[title="' + title + '"]::attr(href)').extract_first()
        if suburl:
            url = self.link_ROC + suburl[suburl.find('../')+3:]
            yield scrapy.Request(url=url, callback=self.contents_ROC_parse)

    def urls_Bank_parse(self, response):
        nexturl = [a.css('::attr(href)').extract_first() for a in response.css('#hlLaw') if not a.xpath('text()').get(default='')]
        if nexturl:
            url = self.link_Bank+nexturl[0]
            yield scrapy.Request(url=url, callback=self.urls_Bank_parse)
        elif response.css('#hlAll::attr(href)').extract_first():
            url = self.link_Bank+response.css('#hlAll::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.contents_Bank_parse)

    def urls_Inter_parse(self, response):
        title = urllib.parse.unquote(response.url[response.url.find('kw=')+3:])
        suburl = [i.css("::attr(href)").extract_first() for i in response.css("table a") if i.xpath('text()').get(default='') == '']
        if suburl:
            url = self.link_Inter+suburl[0][:suburl[0].find('&KeyWord=')]
            yield scrapy.Request(url=url, callback=self.contents_Inter_parse)

    def contents_ROC_parse(self, response):
        if response.css('.law-reg-content *::text'):
            content = [i.strip().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\u3000', '') for i in response.css('.law-reg-content *::text').extract() if i.strip().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\u3000', '')]
            item = ContentItem()
            item['title'] = response.css('#hlLawName::text').extract_first(default='Missing')
            item['resource'] = 'ROC'
            item['url'] = response.url
            if response.css('#trLNNDate td::text').extract_first():
                item['time'] = response.css('#trLNNDate td::text').extract_first().strip()
            else:
                response.css('#trLNODate td::text').extract_first(default='Missing').strip()
            item['content'] = content
            return item

    def contents_Bank_parse(self, response):
        if response.css('.title td::text').extract():
            time = [i.strip() for i in response.css('.title td::text').extract() if i.strip()]
            content = [i.strip().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\u3000', '') for i in response.css('.ContentArea-law *::text').extract() if i.strip().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\u3000', '')]
            item = ContentItem()
            item['title'] = response.css('.title a::text').extract_first(default='Missing')
            item['resource'] = 'Bank'
            item['url'] = response.url
            item['time'] = time[0]
            item['content'] = content[1:]
            return item

    def contents_Inter_parse(self, response):
        if response.css("#ctl00_cp_content_divLawContent08 b::text").extract():
            time = response.css("#ctl00_cp_content_lawheader1_trAmdDate td::text").extract_first(default='Missing').strip()
            content = [i.strip().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\u3000', '') for i in response.css("#ctl00_cp_content_divLawContent08 b::text").extract() if i.strip().replace('\xa0', '').replace('\r', '').replace('\n', '').replace('\u3000', '')]
            item = ContentItem()
            item['title'] = response.css("table tr")[0].css("td::text").extract_first(default='Missing')
            item['resource'] = 'Inter'
            item['url'] = response.url
            item['time'] = time
            item['content'] = content
            return item