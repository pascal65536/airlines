import urllib.request
from urllib.request import urlopen
from lxml.html import fromstring
import cssselect
import json
from datetime import datetime, date, time


def main(parse_url):
    print(parse_url)

    # set of months name
    months = {'January','February','March','April','May','June','July','August','September','October','November','December'}

    # selector
    name_css = '#post-45659 > div.entry-content'
    
    month = ''
    airlines = []
    airline = {}
    
    f = urlopen(parse_url)
    details_html = urlopen(parse_url).read().decode('utf-8')
    details_doc = fromstring(details_html)

    # all lines in div
    lines = details_doc.cssselect(name_css)[0].getchildren()
    
    for line in lines:
           
        # find strind contents month name
        if line.text_content() in months:
            month = line.text_content()

        scrapping_data = line.text_content()

        # data for scrapping contents ':' and month defined later
        if ':' in scrapping_data and not month == '':           
            scrapping_list = scrapping_data.split(':')
            
            if scrapping_list[0] == 'Airline' and len(airline) > 1:
                airlines.append(airline)
                airline = {}

            
            airline[scrapping_list[0]] = scrapping_list[1].strip()
            airline['month'] = month
            airline['created'] = datetime.now()

            images = line.cssselect('img')
            
            for item in images:
                airline['picture'] = item.get('src')

    airlines.append(airline)
    return airlines

def show(lists):
    for list in lists:
        print(list)

if __name__ == '__main__':
    
    # scrapping page
    url = 'https://internationalflyguy.com/2018/12/31/buh-bye-the-airlines-we-lost-in-2018/'

    scrap = main(url)
    
    show(scrap)
