import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tutorial.items import NrgItem

class MySpider(CrawlSpider):

    MIN_PARAGRAPH_LENGTH = 10

    name = 'energy-central-example'
    allowed_domains = ['energycentral.com']
    start_urls = ['https://energycentral.com/news/cubans-wary-sharp-rise-electricity-prices-starting-january']

    rules = (
        Rule(callback='parse_item'),
    )

    def parse_item(self, response):
        
        item = NrgItem() # scrapy.Item()
        item['src_url'] = response.url
        print(item['src_url'])

        # item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        # item['name'] = response.xpath('//td[@id="item_name"]/text()').get()
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
        #item['link_text'] = response.meta['link_text']
        # url = response.xpath('//td[@id="additional_data"]/@href').get()
        #return response.follow(url, self.parse_additional_page, cb_kwargs=dict(item=item))

        content = response.css("div.read-more-left p::text").getall()
        paragraphs = []
        for para in content:
            paragraphs.append(para)
        
        item['paragraphs'] = paragraphs

        yield(item)

    # def parse_additional_page(self, response, item):
    #     item['additional_data'] = response.xpath('//p[@id="additional_data"]/text()').get()
    #     return item