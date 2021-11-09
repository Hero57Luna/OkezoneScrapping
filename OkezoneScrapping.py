import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd

news_headline = []
news_category = []
news_created = []
news_url = []
next_page_url = []
one_year_date = []
one_year_url = []


def get_news_url(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    body = soup.find('body')

    for newsURL in body.find_all('h4', class_='f17'):
        news_url.append(newsURL.a.get('href'))


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


def get_next_page_url(url):
    increment = 0

    for i in range(5):
        new_url = url + str(increment)
        source = requests.get(new_url).text
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        list_berita = body.find('li', class_='col-md-12 p-nol m-nol hei-index')

        if list_berita:
            next_page_url.append(new_url)
            increment += 10
        else:
            break


def get_one_year_data(url):
    oneyear = pd.date_range(start='2021-11-07', end='2021-11-09')
    final_date = oneyear.strftime('/%Y/%m/%d/')
    for date in range(len(final_date)):
        new_url = url + final_date[date]
        one_year_url.append(new_url)


def main(url):
    get_one_year_data(url)
    for i in range(len(one_year_url)):
        get_next_page_url(one_year_url[i])
    for j in range(len(next_page_url)):
        get_headline(next_page_url[j])
        get_category(next_page_url[j])
        get_date_created(next_page_url[j])
        get_news_url(next_page_url[j])
    for i in range(len(news_headline)):
        print("============================")
        print("Headline: " + news_headline[i])
        print("Category: " + news_category[i])
        print("Created: " + news_created[i])
        print("URL: " + news_url[i])
        print("============================")


if __name__ == '__main__':
    main('https://lifestyle.okezone.com/indeks')
