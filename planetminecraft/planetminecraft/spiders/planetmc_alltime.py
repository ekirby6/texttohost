import scrapy  # library used for web scraping
from datetime import date, datetime  # to get the date & time stamp of the scrape


def convert_to_int(str_num):  # used to convert the map stats numbers into numeric integer forms
    if str_num[-1:] == 'k':  # check if the last digit is k
        return int(float(str_num[:-1]) * 1000)  # Remove the last digit with [:-1], then convert to integer
    elif str_num[-1:] == 'm':  # check if the last digit is m
        return int(float(str_num[:-1]) * 1000000)  # Remove the last digit with [:-1], then convert to integer
    else:  # just in case the number doesn't have an m or k
        return int(str_num)  # simply converts to integer


def get_stats(r_stats, search_term, tag):
    if r_stats.find(search_term) != -1:   # if stat is present
        r5s = r_stats[r_stats.find(search_term):]
        start = r5s.find('<' + tag + '>') + len('<' + tag + '>')
        end = r5s.find('</' + tag + '>')
        return r5s[start:end]
    else:   # stat=0 if not included in string
        return str(0)


class MapSpider(scrapy.Spider):
    name = "pmc alltime maps"  # call web scraping in the terminal: scrapy crawl "pmc alltime maps" -o pmcalltime.json

    def start_requests(self):
        # urls for most popular maps: all time
        urls = ['https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=1',
                'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=2']  # testing
        # urls = [
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=1',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=2',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=3',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=4',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=5',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=6',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=7',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=8',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=9',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=10',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=11',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=12',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=13',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=14',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=15',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=16',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=17',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=18',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=19',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=20',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=21',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=22',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=23',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=24',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=25',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=26',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=27',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=28',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=29',
        #     'https://www.planetminecraft.com/projects/?order=order_popularity&time_machine=all_time&p=30'
        # ]

        for url in urls:      # the urls we are scraping
            yield scrapy.Request(url=url, callback=self.parse)   # parses the urls by attributes

    def parse(self, response):
        page = response.url[response.url.find('&p=') + 3:]  # grabs the page number from the website url
        filename = 'pmcalltimemaps-%s.html' % page  # need to name the files with different names so use the page number
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)  # logs that it was actually saved

        r2 = response.css(".content")  # found using selector gadget, the center section. start big & get smaller

        for map in r2.css(".r-info"):  # iterates through all of the maps in the selected section
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
            map_timeaccessed = datetime.now().time()
            map_source = "planetminecraft all-time best"

            # map stats (get in string format, then convert to int)
            r4s = map.css(".r-stats").get()  # string that is parsed to get stats
            tag = 'span'  # tag that is used to parse stats
            map_views = convert_to_int(get_stats(r4s, 'visibility', tag))
            map_downloads = convert_to_int(get_stats(r4s, 'get_app', tag))
            map_comments = convert_to_int(get_stats(r4s, 'chat_bubble', tag))

            yield {
                'title': map_title,
                'subtitle': map_subtitle,
                'author': map_author,
                'page': page,
                'page URL': map_pageurl,
                'map description URL': map_descriptionurl,
                'date of last update': map_lastupdateddate,
                'date accessed': map_dateaccessed,
                'time accessed': map_timeaccessed,
                'map source': map_source,
                'views': map_views,
                'downloads': map_downloads,
                'comments': map_comments
            }
