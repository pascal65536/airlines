#import sys
#import re
import requests
from bs4 import BeautifulSoup
#import json


def parse_title(url_title, separator):
    r = requests.get(url_title)
    soup = BeautifulSoup(r.content, 'html.parser')
    ret = (lambda f, s: f.split(s, 1)[:1][0] if s != '' else f)(soup.title.string.strip(), separator)
    return ret


def parse_liveinternet(url, separator, count):
    orders_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.findAll("table")
    table7 = tables[7]
    for row in table7.findAll("tr"):
        cells = row.findAll("td")
        try:
            cells[1].find('a', href=True)['href']
            cells[2]
        except IndexError:
            pass
        except TypeError:
            pass
        else:
            url_cells = cells[1].find('a', href=True)['href']
            title = parse_title(url_cells, separator)

            order_info = {'url': url_cells,
                          'title': title,
                          'count': int(re.sub('[,]', '', cells[2].find(text=True)))
                          }

            # get rid of duplicates
            if title not in [i['title'] for i in orders_list]:
                orders_list.append(order_info)

        if len(orders_list) > count:
            break

    return orders_list


# returns the site name, date and number of visitors
def parse_liveinternet_head(url):
    orders_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.findAll("table")

    name = soup.findAll("a")[23].find(text=True)

    table5 = tables[5]

    for row in table5.findAll("tr"):
        cells = row.findAll("td")
        data_verbose = cells[1].find(text=True)

    pageviews = tables[7].findAll("tr")[1].findAll("td")[2].find(text=True)
    visitors = tables[7].findAll("tr")[3].findAll("td")[2].find(text=True)

    order_info = {'name': name,
                  'data_verbose': data_verbose,
                  'pageviews': int(re.sub('[,]', '', pageviews)),
                  'visitors': int(re.sub('[,]', '', visitors))
                  }
    orders_list.append(order_info)

    return orders_list


def url_index(base_url, date_url):
    return f'https://www.liveinternet.ru/stat/{base_url}/index.html?date={date_url}'


def url_pages(base_url, date_url):
    return f'https://www.liveinternet.ru/stat/{base_url}/pages.html?date={date_url}'


def url_last_pages(base_url, date_url):
    return f'https://www.liveinternet.ru/stat/{base_url}/last_pages.html?date={date_url}'


def say_visitors(visitors, zavet_visitors):
    return (
        f'За этот день сайт ГН постетили {visitors} человек, '
        f'а по заветам к нам должны заходить {zavet_visitors}. '
        f'Это {(visitors/zavet_visitors*100):.2f}% от цели.'
    )


def say_pageviews(pageviews, zavet_pageviews):
    return (
        f'За этот день сайт ГН просмотрели {pageviews} страниц, '
        f'а по заветам у нас должны смотреть {zavet_pageviews}. '
        f'Это {(pageviews/zavet_pageviews*100):.2f}% от цели.'
    )


def data_say(visitors, pageviews, zavet_visitors, zavet_pageviews):
    orders_list = []
    order_info = {
        'say_visitors': say_visitors(visitors, zavet_visitors),
        'say_pageviews': say_pageviews(pageviews, zavet_pageviews),
    }
    orders_list.append(order_info)
    return orders_list


def anatomy_site(data, n):
    return (
        f'{data[n][0][0]["name"]} -- {data[n][0][0]["visitors"]} посетителей \n\n'
        f'ТОП-новости: \n'
        f'{data[n][1][0]["title"]} -- {data[n][1][0]["count"]} \n'
        f'{data[n][1][1]["title"]} -- {data[n][1][1]["count"]} \n'
        f'{data[n][1][2]["title"]} -- {data[n][1][2]["count"]} \n\n\n'
    )


def anatomy(file_name):
    with open('data.json', 'r') as f_out:
        data = json.load(f_out)

    anatomy = (
        f'{data[0][0][0]["data_verbose"]} \n\n'
        f'{anatomy_site(data, 0)}'
        f'{data[0][2][0]["say_visitors"]} \n'
        f'{data[0][2][0]["say_pageviews"]} \n\n\n'
        f'{anatomy_site(data, 1)}'
        f'{anatomy_site(data, 2)}'
        f'{anatomy_site(data, 3)}'
    )

    with open(file_name+'.txt', 'w') as f_out:
        f_out.write(anatomy)


def main1(date_url, zavet_pageviews, zavet_visitors, report_length):
    main_data = []

    # website address, page with data, statistics page, separator
    lists = [
        ('gornovosti.ru', url_index, url_pages, ''),
        ('krsk.aif.ru', url_index, url_pages, ' | '),
        ('krasnoyarsk.dkvartal.ru', url_index, url_last_pages, '. - '),
        ('prmira.ru', url_index, url_pages, ' | ')
    ]

    i = 0
    for list in lists:
        data = []
        website_address = list[0]
        page_with_data = list[1]
        statistics_page = list[2]
        separator = list[3]

        data_top = parse_liveinternet_head(page_with_data(website_address, date_url))
        data.append(data_top)
        data.append(parse_liveinternet(statistics_page(website_address, date_url), separator, report_length))
        if website_address == 'gornovosti.ru':
            data.append(data_say(data_top[0]['visitors'], data_top[0]['pageviews'], zavet_visitors, zavet_pageviews))
        main_data.append(data)

        i += 1
        print(f'{100/len(list)*i}%')

    with open('data.json', 'w') as f_in:
        json.dump(main_data, f_in, indent=4, ensure_ascii=False)


def main(url):
    print(url)
    orders_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    mydivs = soup.findAll("div", { "class" : "entry-content" })
    #p = soup.find("p")
    #h1 = soup.findAll("h1", style="text-align: center;")
    print(mydivs[0].next_element)


if __name__ == '__main__':
    url = 'https://internationalflyguy.com/2018/12/31/buh-bye-the-airlines-we-lost-in-2018/'

    main(url)

