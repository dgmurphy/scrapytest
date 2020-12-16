import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import NrgItem

class MySpider(CrawlSpider):

    MIN_PARAGRAPH_LENGTH = 10

    name = 'power-eng'
    allowed_domains = ['power-eng.com']
    start_urls = ['https://www.power-eng.com/2020/09']

    link_allow_regex = re.compile(r"https:\/\/www.power-eng.com\/2020\/09.*")

    rules = (
        Rule(LinkExtractor(allow=link_allow_regex), callback='parse'),
    )

    def parse(self, response):
        
        item = NrgItem() # scrapy.Item()
        item['src_url'] = response.url

        content = response.xpath('//*[@id="top-level"]/descendant-or-self::*/text()').getall()
        paragraphs = []
        for para in content:
            if len(para.strip()) > self.MIN_PARAGRAPH_LENGTH:
                paragraphs.append(para)
        
        item['paragraphs'] = paragraphs
        yield(item)

        anchors = response.css('.cl-site__content a')
        for a in anchors:
            yield response.follow(a, callback=self.parse)
