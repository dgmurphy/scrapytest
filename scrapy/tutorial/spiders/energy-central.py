import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import NrgItem
from datetime import datetime
from scrapy_splash import SplashRequest


class MySpider(CrawlSpider):

    MIN_PARAGRAPH_LENGTH = 1
    SPIDER_NAME = 'energy-central'
    name = SPIDER_NAME

    allowed_domains = ['energycentral.com']

    # start_url_prefix = 'https://energycentral.com/#keywords%3D%26entity_bundles%3D-all%26sort_type%3Ddate_newest%26topics%3D-all%26page%3D'
    start_url_prefix = 'https://energycentral.com/news/#keywords%3D%26entity_bundles%3Dnode__allnews%26sort_type%3Ddate_newest%26topics%3D-all%26page%3D'

    start_urls = []
    for n in range(0, 6686):
        start_url = start_url_prefix + str(n)
        start_urls.append(start_url)

    #start_urls = ['https://energycentral.com/c/ee/iea-releases-energy-efficiency-2020-report']

    link_allow_regex = re.compile(r"https:\/\/energycentral.com.*")

    rules = (
        Rule(LinkExtractor(allow=link_allow_regex), callback='parse'),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 5})

    def parse(self, response):
        
        item = NrgItem() # scrapy.Item()
        item['src_url'] = response.url
        item['ingest_date'] = str(datetime.today())
        item['spider_name'] = self.SPIDER_NAME

        content = response.css("div.read-more-left p::text").getall()
        paragraphs = []
        for para in content:
            if len(para.strip()) > self.MIN_PARAGRAPH_LENGTH:
                paragraphs.append(para)
        
        item['paragraphs'] = paragraphs
        item['html'] = response.text
        yield(item)

        related = response.css('span.article-title a')
        for a in related:
            yield response.follow(a, callback=self.parse)

