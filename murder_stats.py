from lxml import html
import requests
import math
import statistics

requests.packages.urllib3.disable_warnings()

def convertList(num_count) : 
    for i in range(len(num_count)) :
        num_count[i] = num_count[i].replace(',','')        
        num_count[i] =  float(num_count[i]);
    return num_count

def crimeStats(num_count) :
    statarr = {}
    statarr[0] = sum(num_count)
    statarr[1] = statistics.mean(num_count)
    statarr[2] = statistics.median(num_count)
    statarr[3] = statistics.stdev(num_count)
    return statarr
   
def printStats(statarr) :
    print "\tTotal: ", statarr[0]
    print "\tMean: ", statarr[1]
    print "\tMedian: ", statarr[2]
    print "\tStandard Deviation: ", statarr[3]
    print "\v"



# Define the page and the tree structure
page = {}
page[0] = requests.get('https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2010/crime-in-the-u.s.-2010/tables/10tbl20.xls')
page[1] = requests.get('https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2011/crime-in-the-u.s.-2011/tables/table-20')
page[2] = requests.get('https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2012/crime-in-the-u.s.-2012/tables/20tabledatadecpdf/table_20_murder_by_state_types_of_weapons_2012.xls')
page[3] = requests.get('https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2013/crime-in-the-u.s.-2013/tables/table-20/table_20_murder_by_state_types_of_weapons_2013.xls')
page[4] = requests.get('https://www.fbi.gov/about-us/cjis/ucr/crime-in-the-u.s/2014/crime-in-the-u.s.-2014/tables/table-20')


murder_count = {}
gun_violence = {}
murder_stats = {}
gun_stats = {}

for j in range(len(page)) : 
    print "\v\v"
    tree = html.fromstring(page[j].content)
    
    # Make lists out of table data using XPath
    murder_count[j] = tree.xpath('//td[@class="odd group1 alignright valignmentbottom numbercell"]/text()')
    gun_violence[j] = tree.xpath('//td[@class="even group2 alignright valignmentbottom numbercell"]/text()')
    
    # Convert any string numerical data into float list 
    murder_count[j] = convertList(murder_count[j])
    gun_violence[j] = convertList(gun_violence[j])
    
    # Get crime stats and print them
    print "Murder Count: "
    murder_stats[j] = crimeStats(murder_count[j])
    printStats(murder_stats[j])

    print "Gun Violence: "
    gun_stats[j] = crimeStats(gun_violence[j])
    printStats(gun_stats[j])


    print "Percent of Total Murders that are Gun Crimes:"
    a = int(1000* gun_stats[j][0]/murder_stats[j][0])/10.0
    print "\t", a, '%', '\v'

   


