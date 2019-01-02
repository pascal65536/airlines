import urllib.request
from urllib.request import urlopen
from lxml.html import fromstring
import cssselect
import json
from datetime import datetime, date, time


def main(parse_url):
    print(parse_url)
    airlines = []
    airline = {'title': title, 'country': country, 'birthday': birthday, 'death': death, 'fleet_size': fleet_size, 'status': status, 'created': created, 'changed': changed}
    f = urlopen(parse_url)
    details_html = urlopen(parse_url).read().decode('utf-8')
    details_doc = fromstring(details_html)

    lines = details_doc.cssselect(name_css)[0].getchildren()
    
    for line in lines:
        if line.text_content() in months:
            month = line.text_content()
            print('--------------------------------------------------------')
            print(line.text_content())
            airline = {
                'title': title,
                'country': country,
                'birthday': birthday,
                'death': month,
                'fleet_size': fleet_size,
                'status': status,
                'created': datetime.now(),
                'changed': changed,
            }

        if 'Year Established:' in line.text_content():
            print( line.text_content() )
        
        airlines.append(airline)

    return airlines
   
    #print(line.text_content())

'''    
    months = details_doc.cssselect('h1[style="text-align: center;"]')
    for month in months:
        print(month)
'''
        
    #text = details_doc.cssselect(name_css)
    #text = escape(details.text_content().strip())
    #details = details_doc.cssselect('p')[0] 


if __name__ == '__main__':
    title = 'title'
    country = 'country'
    birthday = 'birthday'
    death = 'death'
    fleet_size = 'fleet_size'
    status = 'status'
    created = 'created'
    changed = 'changed'
    
    url = 'https://internationalflyguy.com/2018/12/31/buh-bye-the-airlines-we-lost-in-2018/'
    months = {'January','February','March','April','May','June','July','August','September','October','November','December'}
    name_css = '#post-45659 > div.entry-content'

    main(url)
