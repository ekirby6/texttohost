import scrapy
from datetime import date


class ModsSpider(scrapy.Spider):
    name = "cf mods"                 # use the name to call the web scraping in the terminal

    def start_requests(self):
        urls = [
            'https://www.curseforge.com/minecraft/modpacks?page=1',
            'https://www.curseforge.com/minecraft/modpacks?page=2'
        ]

        for url in urls:      # the urls we are scraping
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url[-1]   # grabs the page number from the website url
        # [-1] gives the last character (the page number)
        filename = 'cfmods-%s.html' % page  # need to name the files with different names so use the page number
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)  # logs that it was actually saved

        r2 = response.css(".flex-1")   # found using selector gadget, the center section

        dict_mods = {}     # creating empty dictionary

        for mod in r2.css(".r-info"):   # .lg\:items-center

            mod_title = mod.css(".r-title::text").get()
            mod_subtitle = mod.css(".r-subtitle").css(".r-subject::text").get()
            # mod_author = __ still need to figure this out**
            # mod_description = __ still need to figure out**
            # mod_pageurl = __ still need to figure out**
            # mod_downloadurl = __ still need to figure out**
            mod_lastupdateddate = mod.css(".timeago::text").get()
            mod_dateaccessed = date.today().strftime("%m/%d/%Y")  # date of the scrape in format mm/dd/yyyy
            mod_source = "curseforge"

            index_list = [0]   # .text-xs:nth-child(1) instead of stats
            while mod.css(".r-stats")[3].get().find('i class') != -1:     # views, downloads, comments count
                index_list.append(mod.css(".r-stats")[3].get().find('i class'))
                # what is happening here??***


            dict_mods.update({mod_title:{"Subtitle":mod_subtitle}})
            # stores all the data in the dict, searchable by subtitle
            pass
        print(dict_mods)