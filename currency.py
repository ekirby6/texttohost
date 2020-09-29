#!/usr/bin/python

from lxml import html
import requests
import math
import statistics


url = "http://markets.wsj.com/"
page = requests.get(url)
tree = html.fromstring(page.content)


currency_summary = tree.xpath('//*[@id="glanceCurrencies_Id"]/table/tbody/tr/td/text()')

print '\v'
    
print "EURO"
print '\t',"Last: ",currency_summary[2]
print '\t',"Change: ",currency_summary[3],'\n'

print "YEN"
print '\t',"Last: ",currency_summary[6]
print '\t',"Change: ",currency_summary[7],'\n'

print "POUND"
print '\t',"Last: ",currency_summary[10]
print '\t',"Change: ",currency_summary[11],'\n'

print "AUSTRALIA"
print '\t',"Last: ",currency_summary[14]
print '\t',"Change: ",currency_summary[15],'\n'

print "SWISS FRANC"
print '\t',"Last: ",currency_summary[18]
print '\t',"Change: ",currency_summary[19],'\n'

print '\v'

    

