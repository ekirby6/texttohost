import scrapy  # library used for web scraping
from datetime import date  # used to get the date stamp of the scrape


def convert_to_int(str_num):  # used to convert the map stats numbers into numeric integer forms
    if str_num[-1:] == 'k':  # check if the last digit is k
        return int(float(str_num[:-1]) * 1000)  # Remove the last digit with [:-1], then convert to integer
    elif str_num[-1:] == 'm':  # check if the last digit is m
        return int(float(str_num[:-1]) * 1000000)  # Remove the last digit with [:-1], then convert to integer
    else:  # just in case the number doesn't have an m or k
        return int(str_num)  # simply converts to integer


class MapSpider(scrapy.Spider):
    name = "pmc 7d maps"  # call web scraping in the terminal: scrapy crawl "pmc 7d maps" -o pmc7d.json

    def start_requests(self):
        urls = [
            'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=1',
            'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=2'
        ]
        # urls for most popular maps: last 7 days
        # **need to change this to algorithm!

        for url in urls:      # the urls we are scraping
            yield scrapy.Request(url=url, callback=self.parse)   # parses the urls by attributes

    def parse(self, response):
        page = response.url[-1]   # grabs the page number from the website url
        # [-1] gives the last character (the page number)
        filename = 'pmc7dmaps-%s.html' % page  # need to name the files with different names so use the page number
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)  # logs that it was actually saved

        r3 = response.css(".content")   # found using selector gadget, the center section. start big & get smaller

        for map in r3.css(".r-info"):   # iterates through all of the maps in the selected section
            map_title = map.css(".r-title::text").get()
            map_subtitle = map.css(".r-subtitle").css(".r-subject::text").get()

            # finding map author using the string methods
            str1 = map.css(".contributed").get()
            author_start = str1.find('load">') + 7  # start of author's name in the string
            author_end = str1.find('</a>') - 1  # end of author's name in the string
            map_author = str1[author_start:author_end]  # sliced substring including only the formatted author's name

            # map_description- planetmc doesn't have descriptions so disregard
            map_pageurl = response.url  # the main page url that the map was on, for records
            map_descriptionurl = 'www.planetminecraft.com' + map.css(
                ".r-info > a::attr('href')").get()  # link from clicking-in to individual map details
            # map_downloadurl - third party download issues, don't worry about for now
            map_lastupdateddate = map.css(".timeago::text").get()  # date from the last update of the map
            map_dateaccessed = date.today().strftime("%m/%d/%Y")  # date of the scrape in format mm/dd/yyyy
            map_source = "planetminecraft last 7 days best"

            # map stats (get in string format, then convert to int
            str2 = map.css(".r-stats").get()
            str_views = str2[str2.find('visibility') + 23:str2.find('get_app') - 33]  # count of map views
            map_views = convert_to_int(str_views)
            str_downloads = str2[str2.find('get_app') + 20:str2.find('chat_bubble') - 33]  # count of map downloads
            map_downloads = convert_to_int(str_downloads)
            str_comments = str2[str2.find('chat_bubble') + 24:str2.find('</span></div>')]  # count of map comments
            map_comments = convert_to_int(str_comments)

            # **include filter to put a null value ("NA") if a stat is missing??

            # dict_maps = {}  # creating empty dictionary   # would be called above for loop
            # map_dict.update({map_title:{"Subtitle":map_subtitle}})
            # stores all the data in the dict, searchable by subtitle. just need to make empty dict first

            yield {
                'title': map_title,
                'subtitle': map_subtitle,
                'author': map_author,
                'page': page,
                'page URL': map_pageurl,
                'map description URL': map_descriptionurl,
                'date of last update': map_lastupdateddate,
                'date accessed': map_dateaccessed,
                'map source': map_source,
                'views': map_views,
                'downloads': map_downloads,
                'comments': map_comments
            }

        # work on NA stats and algorithm**
