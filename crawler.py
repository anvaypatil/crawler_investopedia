import urllib2
import urllib
from bs4 import BeautifulSoup
import re
import unicodedata as u
import os.path as ospath
import os as os
import sys
import time
import errno

LINK = "http://www.investopedia.com/terms/"


def get_content(soup):
    # create logs
    els = soup.find_all('a', attrs={'data-cat': ['content_list']})
    return els


def crawl(_id):
    soup = get_soup(_id)
    return get_content(soup)


def get_last_page(soup):
    lst_els = soup.find_all('li', attrs={'class': ['pager-last']})
    last_el = str(lst_els[0])
    last = int(str(last_el.split('page=')[1].split('title')[0]).replace('\'', '').replace('\"', '').strip())
    return last


def get_soup(_id):
    url = LINK + _id
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    return soup


def extract():
    for ch in 'abcdefghijklmnopqrstuvwxyz':
        f = open(ch + '.txt', 'w+')
        time.sleep(5)
        last_page = get_last_page(get_soup(ch))
        print "-----------------------------"
        print "Writing data for  " + ch
        print "number of pages: " + str(last_page)
        write_data(ch, f, last_page)
        print "-----------------------------"
        f.close()


def write_data(ch, f, last_page):
    for index in range(last_page):
        els = crawl(ch + '/?page=' + str(index))
        sys.stdout.write('. ')
        print ""
        for data in els:
            sup = u.normalize('NFKD', re.sub('\s+', ' ', data.get_text())).encode('ascii', 'ignore')
            f.write(sup+"\n")


if __name__ == "__main__":
    extract()
