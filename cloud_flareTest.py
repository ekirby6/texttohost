import cfscrape
# Must import the cloudflare-scape library
# See documentation at https://github.com/Anorov/cloudflare-scrape


scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
print(scraper.get("https://www.curseforge.com/minecraft/modpacks").content) # => "<!DOCTYPE html><html><head>..."