import scrapy
from ..items import ModScrappingItem


# This will not work in the repository bc it is missing the settings, items file from scrapy
class CurseforgeSpiderSpider(scrapy.Spider):
    name = 'curseforge'
    start_urls = ['https://www.planetminecraft.com/']


    def parse(self, response):
        items = ModScrappingItem()

        mod_title = response.css('.text-primary-500.text-lg').css('::text').extract()
        mod_author = response.css('.hover\:no-underline.my-auto').css('::text').extract()

        items['mod_title'] = mod_title
        items['mod_author'] = mod_author

        yield items


