import cfscrape
import pandas as pd
import sys
from bs4 import BeautifulSoup

# Mod object for future data manipulation, currently not needed
class Mod:
    def __init__(self, title, author, description, page_num, download_num, latest_update, link):
        self.title = title
        self.author = author
        self.description = description
        self.page_num = page_num
        self.download_num = download_num
        self.latest_update = latest_update
        self.link = link

    def printAll(self):
        print(self.title)
        print(self.author)
        print(self.description)
        print(self.page_num)
        print(self.download_num)
        print(self.latest_update)
        print(self.link)


# initializes cloudflare scraper
scraper = cfscrape.create_scraper()

# initialize data structures
pages = []
mods = []
titles = []
authors = []
descriptions = []
page_nums = []
download_nums = []
latest_updates = []
links = []

# sets how many pages the script will scrape
# How to use in terminal: python cloud_flare.py pagenumber1 pagenumber2
for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    url = "https://www.curseforge.com/minecraft/modpacks?page=" + str(i)
    pages.append(url)

# goes through each page of curseforge in the designated range
page_count = 0
for page in pages:

    page_count += 1

    # Returns html content of page
    content = scraper.get(page).content

    # Convert html content to Beautiful Soup Object
    soup = BeautifulSoup(content, 'html.parser')

    # Get HTML for each div which contains the mod info
    divs = soup.select('.lg\:items-center')

    # scrapes the data from each div containing each individual mod
    div: BeautifulSoup
    for div in divs:
        downloads = div.find(class_='mr-2 text-xs text-gray-500', text=True).string
        a_title = div.find(class_='text-primary-500 font-bold text-lg', text=True).string
        an_author = div.find(class_='text-base leading-normal font-bold hover:no-underline my-auto', text=True).string
        descr = div.find(class_='text-sm leading-snug', text=True).string
        date = div.select_one(".mr-2 .standard-datetime").string

        # Checks if download link is empty
        if not div.select(".px-1 .button"):
            a_link = '0'
        else:
            a_link = page[0:26] + div.select_one(".px-1 .button")['href']

        # appends the scraped data into each list
        titles.append(a_title)
        authors.append(an_author)
        descriptions.append(descr)
        page_nums.append(page_count)
        download_nums.append(downloads)
        latest_updates.append(date)
        links.append(a_link)

# Add all data to a dataframe and export to csv
df = pd.DataFrame()
df['titles'] = titles
df['author'] = authors
df['numOfDownloads'] = download_nums
df['description'] = descriptions
df['page'] = page_nums
df['update'] = latest_updates
df['downloadLinks'] = links
df.to_csv('curseforge.csv')