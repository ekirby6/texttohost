import scrapy                # library used for web scraping
from datetime import date    # used to get the date stamp of the scrape


class MapsSpider(scrapy.Spider):
    name = "pmc alltime maps"                 # use the name to call the web scraping in the terminal: scrapy crawl "_"

    def start_requests(self):
        urls = [
            'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=1',
            'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=2'
        ]
        # urls for most popular maps: all time
        for url in urls:      # the urls we are scraping
            yield scrapy.Request(url=url, callback=self.parse)  # parses the urls by attributes

    def parse(self, response):
        page = response.url[-1]   # grabs the page number from the website url
        # [-1] gives the last character (the page number)
        filename = 'pmcalltimemaps-%s.html' % page  # need to name the files with different names so use the page number
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)  # logs that it was actually saved

        r2 = response.css(".content")   # found using selector gadget, the center section. start big & get smaller

        dict_maps = {}     # creating empty dictionary

        for map in r2.css(".r-info"):     # iterates through all of the maps in the selected section
            map_title = map.css(".r-title::text").get()
            map_subtitle = map.css(".r-subtitle").css(".r-subject::text").get()

            # finding map author using the string methods
            str = map.css(".contributed").get()
            author_start = str.find('load">') + 7  # start of author's name in the string
            author_end = str.find('</a>') - 1     # end of author's name in the string
            map_author = str[author_start:author_end]  #sliced substring including only the formatted author's name

            # map_description- planetmc doesn't have descriptions so disregard
            map_pageurl = response.url  # the main page url that the map was on, for records
            map_descriptionurl = 'www.planetminecraft.com' + map.css(".r-info > a::attr('href')").get() # link from clicking-in to individual map details
            # map_downloadurl - third party download issues, don't worry about for now
            map_lastupdateddate = map.css(".timeago::text").get()    # date from the last update of the map
            map_dateaccessed = date.today().strftime("%m/%d/%Y")  # date of the scrape in format mm/dd/yyyy
            map_source = "planetminecraft all-time best"




            # index_list = [0]
            #
            # if map.css(".r-stats")[3].get().find('i class') != -1:     # views, downloads, comments count
            #     index_list.append(map.css(".r-stats")[3].get().find('i class'))
            # else:
            #     index_list.append("NA")     # appends "NA" if no data is available for views, downloads, or comments
            #     # what is happening here??** need to separate out the 3 icons, put a null value if one is missing

            dict_maps.update({map_title:{"Subtitle":map_subtitle}})
            # stores all the data in the dict, searchable by subtitle
            pass
        print(dict_maps)   # write to csv first and then later json file**
        # work on author and stats and algorithm/dict/storage**

