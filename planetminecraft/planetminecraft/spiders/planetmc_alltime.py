import scrapy                # library used for webscraping
from datetime import date    # used to get the date stamp of the scrape


class MapsSpider(scrapy.Spider):
    name = "pmc alltime maps"                 # use the name to call the web scraping in the terminal

    def start_requests(self):
        urls = [
            'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=1',
            'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=2'
        ]
        # need to make this into an algorithm**
        # urls for most popular maps: all time
        for url in urls:      # the urls we are scraping
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url[-1]   # grabs the page number from the website url
        # [-1] gives the last character (the page number)
        filename = 'pmcalltimemaps-%s.html' % page  # need to name the files with different names so use the page number
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)  # logs that it was actually saved

        r2 = response.css(".content")   # found using selector gadget, the center section

        dict_maps = {}     # creating empty dictionary

        for map in r2.css(".r-info"):     # iterates through all of the maps in the selected section
            map_title = map.css(".r-title::text").get()
            map_subtitle = map.css(".r-subtitle").css(".r-subject::text").get()
            # map_author = map.css(".membertip activity_name tipso_style").get() **need to figure out**
            # map_description = __ still need to figure out**
                # planetmc doesn't really have descriptions so unsure what chase wants**
            map_pageurl = response.url
            map_descriptionurl = 'www.planetminecraft.com' + map.css(".r-info > a::attr('href')").get()
            # map_downloadurl = _ still need to figure out**
                # follow descriptionurl link, then it's .third-party-download**
            map_lastupdateddate = map.css(".timeago::text").get()
            map_dateaccessed = date.today().strftime("%m/%d/%Y")  # date of the scrape in format mm/dd/yyyy
            map_source = "planetminecraft all-time best"

            index_list = [0]
            while map.css(".r-stats")[3].get().find('i class') != -1:     # views, downloads, comments count
                index_list.append(map.css(".r-stats")[3].get().find('i class'))
                # what is happening here??**

            dict_maps.update({map_title:{"Subtitle":map_subtitle}})
            # stores all the data in the dict, searchable by subtitle
            pass
        print(dict_maps)   # want to write to csv file**
