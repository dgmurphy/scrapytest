# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NrgItem(scrapy.Item):
    # define the fields for your item here like:
    documentURI = scrapy.Field()
    paragraphs = scrapy.Field()
    content = scrapy.Field()
    ingestDate = scrapy.Field()
    ingestSource = scrapy.Field()
    
