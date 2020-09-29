from bs4 import BeautifulSoup as bs
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome('C:\Users\Liz\Downloads\chromedriver_win32\chromedriver.exe')
driver.get("https://twitter.com/24x7chess")
soup = bs(driver.page_source, "lxml")

driver.quit()
for title in soup.select("#page-container"):
    name = title.select(".ProfileHeaderCard-nameLink")[0].text.strip()
    location = title.select(".ProfileHeaderCard-locationText")[0].text.strip()
    tweets = title.select(".ProfileNav-value")[0].text.strip()
    following = title.select(".ProfileNav-value")[1].text.strip()
    followers = title.select(".ProfileNav-value")[2].text.strip()
    likes = title.select(".ProfileNav-value")[3].text.strip()
    print(name, location, tweets, following, followers, likes)

