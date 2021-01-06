# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AcmItem(scrapy.Item):
    title= scrapy.Field()
    authors=scrapy.Field()
    journal=scrapy.Field()
    laboratoire=scrapy.Field()
    date_pub=scrapy.Field()
 
    pass
