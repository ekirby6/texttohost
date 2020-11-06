# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlanetminecraftItem(scrapy.Item):
    # define the fields for your item here:
    title = scrapy.Field()
    subtitle = scrapy.Field()
    author = scrapy.Field()
    page = scrapy.Field()
    page_URL = scrapy.Field()
    map_description_URL = scrapy.Field()
    date_of_last_update = scrapy.Field()
    date_accessed = scrapy.Field()
    time_accessed = scrapy.Field()
    map_source = scrapy.Field()
    views = scrapy.Field()
    downloads = scrapy.Field()
    comments = scrapy.Field()