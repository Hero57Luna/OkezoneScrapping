from bs4 import BeautifulSoup
from time import sleep
import requests
import pandas as pd


news_headline = []
news_category = []
news_created = []
news_url = []
next_page_url = []
one_year_date = []
indeks_url = []
all_news_url = []


def get_one_year_url(url):
    oneyear = pd.date_range(start='2021-11-09', end='2021-11-10')
    final_date = oneyear.strftime('/%Y/%m/%d/')
    for date in range(len(final_date)):
        new_url = url + final_date[date]
        indeks_url.append(new_url)


def get_next_page_url():
    for year in range(len(indeks_url)):
        new_url = indeks_url[year]
        increment = 0
        for i in range(2):
            url_new = new_url + str(increment)
            source = requests.get(new_url).text
            soup = BeautifulSoup(source, 'lxml')
            body = soup.find('body')
            list_berita = body.find('li', class_='col-md-12 p-nol m-nol hei-index')

            if list_berita:
                next_page_url.append(url_new)
                increment += 10
            else:
                break
            sleep(10)


def get_news():
    for all_url in range(len(next_page_url)):
        source = requests.get(next_page_url[all_url]).text
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        for headline_index in body.find_all('h4', class_='f17'):
            if headline_index:
                news_headline.append(headline_index.text.strip())

            else:
                break

        for category_index in body.find_all(class_='c-news'):
            if category_index:
                news_category.append(category_index.a.text)

            else:
                break

        for time_index in body.find_all('time', class_='category-hardnews f12'):
            if time_index:
                unwanted = time_index.find('span', class_='c-news')
                unwanted.extract()
                news_created.append(time_index.text.strip())

            else:
                break

        for url_index in body.find_all('h4', class_='f17'):
            if url_index:
                news_url.append(url_index.a.get('href'))
            else:
                break
        sleep(10)


def get_all_news_url(url):
    increment = 0
    for i in range(5):
        increment += 1
        formatted_url = url + f'?page={increment}'
        source = requests.get(formatted_url).text
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        no_active = body.find('div', class_='next noactive')
        next_button = body.find('div', class_='next')

        if next_button:
            all_news_url.append(formatted_url)
            if no_active:
                break
        elif not next_button:
            all_news_url.append(url)
            break
        else:
            break
        sleep(10)


def get_news_content():
    for i in range(len(all_news_url)):
        source = requests.get(all_news_url[i]).text
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        news_content = body.find('div', class_='read')
        for text_news in news_content.find_all('p'):
            print(text_news.text.strip())
        sleep(10)


def main():
    print("Getting valid URL...")
    #  get_one_year_url(url)
    indeks_url.append('https://news.okezone.com/indeks?tgl=11&bln=10&thn=2021&button=GO')
    get_next_page_url()
    print("Done")
    print("Displaying data...")
    get_news()
    for i in range(len(news_headline)):
        print("============================")
        print("Headline: " + news_headline[i])
        print("Category: " + news_category[i])
        print("Created: " + news_created[i])
        print("URL: " + news_url[i])
        print("============================")


if __name__ == '__main__':
    get_all_news_url('https://nasional.okezone.com/read/2021/11/13/337/2501145/presiden-jokowi-tanam-pohon-kayu-putih-di-kawasan-gunung-pepe')
    get_news_content()
