# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PentestItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    link_url = scrapy.Field()
    comment = scrapy.Field()
    location_url = scrapy.Field()
    form = scrapy.Field()
    method = scrapy.Field()
    email = scrapy.Field()
    cookies = scrapy.Field()

