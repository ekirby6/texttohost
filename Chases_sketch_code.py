import scrapy


class QuotesSpider(scrapy.Spider):
    name = "maps"

    def start_requests(self):
        urls = [
            'https://www.planetminecraft.com/projects/?p=1/',
            'https://www.planetminecraft.com/projects/?p=2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2][3:]
        filename = 'mcmaps-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        r2 = response.css(".content")

        dict_maps = {}

        for map in response.css(".r-info"):
            map_title = map.css(".r-title::text").get()
            map_subtitle = map.css(".r-subtitle").css(".r-subject::text").get()

            index_list = [0]
            while map.css(".r-stats")[3].get().find('i class') != -1:
                index_list.append(map.css(".r-stats")[3].get().find('i class'))


            dict_maps.update({map_title:{"Subtitle":map_subtitle}})
            pass
        print(dict_maps)
