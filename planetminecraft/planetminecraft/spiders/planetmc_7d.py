import scrapy
from datetime import date


class MapsSpider(scrapy.Spider):
    name = "pmc 7d maps"                 # use the name to call the web scraping in the terminal

    def start_requests(self):
        urls = [
            'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=1',
            'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=2'
        ]
        # urls for most popular maps: last 7 days
        for url in urls:      # the urls we are scraping
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url[-1]   # grabs the page number from the website url
        # [-1] gives the last character (the page number)
        filename = 'pmc7dmaps-%s.html' % page  # need to name the files with different names so use the page number
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)  # logs that it was actually saved

        r2 = response.css(".content")   # found using selector gadget, the center section

        dict_maps = {}     # creating empty dictionary

        for map in r2.css(".r-info"):
            map_title = map.css(".r-title::text").get()
            map_subtitle = map.css(".r-subtitle").css(".r-subject::text").get()
            # map_author = __ still need to figure this out**
            # map_description = __ still need to figure out**
            # map_pageurl = __ still need to figure out**
            # map_downloadurl = __ still need to figure out**
            map_lastupdateddate = map.css(".timeago::text").get()
            map_dateaccessed = date.today().strftime("%m/%d/%Y")  # date of the scrape in format mm/dd/yyyy
            map_source = "planetminecraft"

            index_list = [0]
            while map.css(".r-stats")[3].get().find('i class') != -1:     # views, downloads, comments count
                index_list.append(map.css(".r-stats")[3].get().find('i class'))
                # what is happening here??***

            dict_maps.update({map_title:{"Subtitle":map_subtitle}})
            # stores all the data in the dict, searchable by subtitle
            pass
        print(dict_maps)
