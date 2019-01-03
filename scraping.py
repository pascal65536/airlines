from urllib.request import urlopen
from lxml.html import fromstring
import cssselect
import json
from datetime import datetime, date, time


def main(parse_url):

    # set of months name
    MONTHS = {'January','February','March','April','May','June','July','August','September','October','November','December'}
    # selector
    NAME_CSS = '#post-45659 > div.entry-content'
    
    month = ''
    airline = {}
    airlines = []
    pictures = []
    
    # f = urlopen(parse_url)
    details_html = urlopen(parse_url).read().decode('utf-8')
    details_doc = fromstring(details_html)

    # all lines in div
    lines = details_doc.cssselect(NAME_CSS)[0].getchildren()
    
    for l in lines:
        # find string contents month name
        if l.text_content() in MONTHS:
            month = l.text_content()

        scrapping_data = l.text_content()

        # collect pictures in list
        images = l.cssselect('img')
        for item in images:
            pic = item.get('src')
            if pic not in pictures:
                pictures.append(pic)

        # data for scrapping contents ':' and month defined later
        if ':' in scrapping_data and not month == '':
            # error in web page
            # *ext contents title airline
            key, value, *ext = scrapping_data.split(':')

            # key 'Airline' is signal: adding dict an create new
            if key == 'Airline' and len(airline) > 1:
                # pop is list pictures
                if not len(pictures) == 0:
                    airline['picture'] = pictures.pop(0)
                airlines.append(airline)
                airline = {}
                
            # fix error
            if not len(ext) == 0:
                airline[key] = value.replace('Airline', '').strip()
                if not len(pictures) == 0:
                    airline['picture'] = pictures.pop(0)
                airlines.append(airline)
                airline = {'Airline': ext[0].strip()}
            else:
                value = value.strip()

            airline[key] = value
            airline['month'] = month
            airline['created'] = datetime.now()

    # last data is last airlines and picture
    airline['picture'] = pictures.pop(0)
    airlines.append(airline)
    
    return airlines


def show(lst):
    for l in lst:
        #pass
        print(l)

        
if __name__ == '__main__':
    # scrapping page
    url = 'https://internationalflyguy.com/2018/12/31/buh-bye-the-airlines-we-lost-in-2018/'
    scrap = main(url)
    show(scrap)
