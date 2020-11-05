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
    name = "seven_day"  # call web scraping in the terminal: scrapy crawl "pmc 7d maps" -o pmc7d.json

    def start_requests(self):
        urls = [
            'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=3'
            # ,
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=2',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=3',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=4',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=5',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=6',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=7',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=8',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=9',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=10',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=11',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=12',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=13',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=14',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=15',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=16',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=17',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=18',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=19',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=20',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=21',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=22',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=23',
            # 'https://www.planetminecraft.com/projects/?time_machine=last7d&order=order_popularity&p=24'
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
        print('STARTING INFO SECTION')
        print(r3.css(".r-info").get())
        print('ENDING INFO SECTION')
        map_dict = {}
        i = 0

        for map in r3.css(".r-info"):   # iterates through all of the maps in the selected section

            print('STARTING MAP')
            print(map.get())
            print('ENDING MAP')
            i += 1
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
            if str2.find('visibility') != -1 and str2.find('get_app') != -1 and str2.find('chat_bubble') != -1:
                # if all 3 fields present
                str_views = str2[str2.find('visibility') + 23:str2.find('get_app') - 33]  # count of map views
                str_downloads = str2[str2.find('get_app') + 20:str2.find('chat_bubble') - 33]  # count of map downloads
                str_comments = str2[str2.find('chat_bubble') + 24:str2.find('</span></div>')]  # count of map comments
            elif str2.find('visibility') != -1 and str2.find('get_app') != -1:  # if have views & downloads
                str_views = str2[str2.find('visibility') + 23:str2.find('get_app') - 33]
                str_downloads = str2[str2.find('get_app') + 20:str2.find('</div>') - 8]
                str_comments = 0
            elif str2.find('visibility') != -1 and str2.find('chat_bubble') != -1:  # if have views & comments
                str_views = str2[str2.find('visibility') + 23:str2.find('</span></div>') - 59]
                str_downloads = 0
                str_comments = str2[str2.find('chat_bubble') + 24:str2.find('</span></div>')]
            elif str2.find('visibility') != -1:  # if only have views (base case)
                # always have at least views to be on the popular/best list
                str_views = str2[str2.find('visibility') + 23:str2.find('</div>') - 9]
                str_downloads = 0
                str_comments = 0
            else:  # if have none of the 3 fields (edge case)
                str_views = 0
                str_downloads = 0
                str_comments = 0
            map_views = convert_to_int(str_views)  # converting string stats to meaningful integers
            map_downloads = convert_to_int(str_downloads)
            map_comments = convert_to_int(str_comments)

            # **include filter to put a null value ("NA") if a stat is missing??

            # dict_maps = {}  # creating empty dictionary   # would be called above for loop
            # map_dict.update({map_title:{"Subtitle":map_subtitle}})
            # stores all the data in the dict, searchable by subtitle. just need to make empty dict first

            my_dict = {
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
            print(my_dict)
            map_dict[str(i)] = my_dict

        # **work on NA stats filter, update page number, and algorithm using .pagination_next button**
        # **insert if statement checking if page = last_page_num then output status = Complete, else status = Fail
            # send out date & time, page, last_page_num, and source name