import locale
from bs4 import BeautifulSoup
import requests

news_headline = []
news_category = []
news_created = []
locale.setlocale(locale.LC_ALL, 'en-US')

def get_headline(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    body = soup.find('body')

    for headline in body.find_all('h4', class_='f17'):
        news_headline.append(headline.text.strip())

    return news_headline


def get_category(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    body = soup.find('body')

    for category in body.find_all(class_='c-news'):
        news_category.append(category.a.text)

    return news_category


def get_date_created(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    body = soup.find('body')

    for time in body.find_all('time', class_='category-hardnews f12'):
        unwanted = time.find('span', class_='c-news')
        unwanted.extract()
        news_created.append(time.text.strip())


def clean_date(date):
    pass


if __name__ == '__main__':
    #  get_headline('https://lifestyle.okezone.com/indeks')
    #  get_category('https://lifestyle.okezone.com/indeks')
    #  get_date_created('https://lifestyle.okezone.com/indeks')
    clean_date(get_date_created('https://lifestyle.okezone.com/indeks'))
