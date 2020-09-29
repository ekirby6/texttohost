from lxml import html
import requests
import math
import statistics


print "\v"

city_list = (
    'canton',
    'cincinnati',
    'rochester',
    'richmond',
    'fort lauderdale',
    'columbus',
    'hilton head',
    'yigo',
    'atlanta'
    
    
);

url_list = (
    'https://www.wunderground.com/us/oh/canton/zmw:44701.1.99999',
    'https://www.wunderground.com/us/oh/cincinnati/zmw:45268.1.99999', 
    'https://www.wunderground.com/us/ny/rochester/zmw:14602.1.99999',
    'https://www.wunderground.com/cgi-bin/findweather/getForecast?query=pws:KVAFAIRF41',
    'https://www.wunderground.com/cgi-bin/findweather/getForecast?query=pws:KFLFORTL107',
    'https://www.wunderground.com/q/zmw:43085.2.99999',
    'https://www.wunderground.com/us/sc/hilton-head/zmw:29925.2.99999',
    'https://www.wunderground.com/q/zmw:96929.2.99999',
    'https://www.wunderground.com/US/GA/Atlanta.html'
  
);


city = str.lower(raw_input('City:  '))

for i in range(len(city_list)) :
    if city == city_list[i] : 
        page = requests.get(url_list[i])

tree = html.fromstring(page.content)
wdata = tree.xpath('//span[@class="wx-value"]/text()')
precip = tree.xpath('//span[@data-variable="precip_today"]//*[@class="wx-value"]/text()')
wind = tree.xpath('//*[@id="windCompassSpeed"]/span/text()')
humid = tree.xpath('//span[@data-variable="humidity"]//*[@class="wx-value"]/text()')


print "\v"

print "Temperature Data \n"
print "\t Current: ", wdata[5], " F"
print "\t Feel: ", wdata[6], " F"

print "\nWeather Conditions \n"
print "\t Weather: ", wdata[4]
print "\t Precip.: ", precip[0], " in"
print "\t Wind: ", wind[0], " mph"
print "\t Humidity: ", humid[0], "%"

print "\v"

