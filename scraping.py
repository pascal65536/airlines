import urllib.request
from urllib.request import urlopen
from lxml.html import fromstring
import cssselect
import json
from datetime import datetime, date, time
from lxml import etree


def main(parse_url):
    print(parse_url)

    # set of months name
    MONTHS = {'January','February','March','April','May','June','July','August','September','October','November','December'}
    # selector
    NAME_CSS = '#post-45659 > div.entry-content'
    
    month = ''
    airlines = []
    airline = {}
    pictures = []
    
    f = urlopen(parse_url)
    details_html = urlopen(parse_url).read().decode('utf-8')
    details_doc = fromstring(details_html)

    # all lines in div
    lines = details_doc.cssselect(NAME_CSS)[0].getchildren()
    
    for line in lines:           
        # find strind contents month name
        if line.text_content() in MONTHS:
            month = line.text_content()

        scrapping_data = line.text_content()

        images = line.cssselect('img')
        for item in images:
            pic = item.get('src')
            if not pic in pictures:
                pictures.append(pic)

        # data for scrapping contents ':' and month defined later
        if ':' in scrapping_data and not month == '':
            key, value, *ext = scrapping_data.split(':')
       
            if key == 'Airline' and len(airline) > 1:
                if not len(pictures) == 0:
                    airline['picture'] = pictures.pop(0)
                airlines.append(airline)
                airline = {}

            if not len(ext) == 0:
                value = value.replace('Airline', '').strip()
                if not len(pictures) == 0:
                    airline['picture'] = pictures.pop(0)
                airlines.append(airline)
                airline = {'Airline': ext[0].strip()}
            else:
                value = value.strip()

            airline[key] = value
            airline['month'] = month
            airline['created'] = datetime.now()

    airlines.append(airline)
    return airlines


def show(lists):
    for list in lists[:]:
        #pass
        print(list)
        
if __name__ == '__main__':
    # scrapping page
    url = 'https://internationalflyguy.com/2018/12/31/buh-bye-the-airlines-we-lost-in-2018/'
    scrap = main(url)
    show(scrap)
