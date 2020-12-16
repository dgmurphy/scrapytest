import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import NrgItem

class MySpider(CrawlSpider):

    MIN_PARAGRAPH_LENGTH = 10

    name = 'energy-central'
    allowed_domains = ['energycentral.com']
    start_urls = ['https://energycentral.com/news/appalachian-power-plans-power-grid-upgrades-jackson-and-kanawha-counties']

    link_allow_regex = re.compile(r"https:\/\/energycentral.com\/news.*")

    rules = (
        Rule(LinkExtractor(allow=link_allow_regex), callback='parse'),
    )

    def parse(self, response):
        
        item = NrgItem() # scrapy.Item()
        item['src_url'] = response.url

        content = response.css("div.read-more-left p::text").getall()
        paragraphs = []
        for para in content:
            if len(para.strip()) > self.MIN_PARAGRAPH_LENGTH:
                paragraphs.append(para)
        
        item['paragraphs'] = paragraphs
        yield(item)

        related = response.css('span.article-title a')
        for a in related:
            yield response.follow(a, callback=self.parse)

