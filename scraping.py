from urllib.request import urlopen
from lxml.html import fromstring
import json
import datetime


def main(parse_url, parse_year):
    # dict name of fields
    FIELDS = {
        'Airline': 'title',
        'From': 'country',
        'Year Established': 'birthday',
        'Fleet Size': 'fleet_size',
        'Status': 'status'
    }

    # dictionary of months name
    MONTHS = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }

    # selector
    NAME_CSS = '#post-45659 > div.entry-content'

    month = ''
    airline = {}
    airlines = []
    pictures = []

    details_html = urlopen(parse_url).read().decode('utf-8')
    details_doc = fromstring(details_html)

    # all lines in div
    lines = details_doc.cssselect(NAME_CSS)[0].getchildren()

    for l in lines:
        # find string contents month name
        for key in MONTHS.keys():
            if key == l.text_content():
                month = MONTHS[l.text_content()]

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
                airline[FIELDS[key]] = value.replace('Airline', '').strip()
                if not len(pictures) == 0:
                    airline['picture'] = pictures.pop(0)
                airlines.append(airline)
                airline = {FIELDS['Airline']: ext[0].strip()}
            else:
                value = value.strip()

            airline[FIELDS[key]] = value
            airline['death'] = f'{parse_year}-{month}-01T00:00:00'
            airline['created'] = datetime.datetime.now().replace(microsecond=0).isoformat()

    # last data is last airlines and picture
    airline['picture'] = pictures.pop(0)
    airlines.append(airline)

    return airlines


def load_from_json(file_name):
    with open(file_name, 'r', encoding='utf-8-sig') as infile:
        return json.load(infile)


if __name__ == '__main__':
    # scrapping page
    scrap_url = 'https://internationalflyguy.com/2018/12/31/buh-bye-the-airlines-we-lost-in-2018/'
    scrap_year = '2018'
    file_airlines = f'airlines_lost_{scrap_year}.json'
    scrap = main(scrap_url, scrap_year)

    # dump dicts of airlines
    with open(file_airlines, 'w') as file_dump:
        json.dump(scrap, file_dump, indent=2)

    print(scrap == load_from_json(file_airlines))
