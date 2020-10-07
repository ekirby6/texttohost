import scrapy


class QuotesSpider(scrapy.Spider):
    name = "maps"                 # use the name to call the web scraping in the terminal

    def start_requests(self):
        urls = [
            'https://www.planetminecraft.com/projects/?p=1',
            'https://www.planetminecraft.com/projects/?p=2'
        ]
        for url in urls:      # the urls we are scraping
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2][3:]   # grabs the page number from the website url
        # splits the url up by /
        # [-2] gives 2nd from last character (the page number)
        # [3:] starts at 3rd character and goes until end (the page number)
        filename = 'mcmaps-%s.html' % page  # need to name the html files with different names so uses the page number
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)  # logs that it was actually saved

        r2 = response.css(".content")   # found using selectorgadget, the center section

        dict_maps = {}     # creating empty dictionary

        for map in r2.css(".r-info"):
            map_title = map.css(".r-title::text").get()
            map_subtitle = map.css(".r-subtitle").css(".r-subject::text").get()

            index_list = [0]
            while map.css(".r-stats")[3].get().find('i class') != -1:     # views, downloads, comments count
                index_list.append(map.css(".r-stats")[3].get().find('i class'))
                # what is happening here??***


            dict_maps.update({map_title:{"Subtitle":map_subtitle}})
            # stores all the data in the dict, searchable by subtitle
            pass
        print(dict_maps)
