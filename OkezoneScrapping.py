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


def get_news_url(url):
    for i in range(3):
        current_url = ''
        source = requests.get(url).text
        print(url)
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        url_div = body.find('div', class_='next')
        try:
            next_button = url_div.find('span', class_='nextssdh')
            if next_button.text == 'Selanjutnya':
                new_url = url_div.a.get('href')
                current_url = new_url
                print(current_url)
                sleep(10)
                break
            else:
                break
        except AttributeError:
            break


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
    get_news_url('https://news.okezone.com/read/2021/11/11/18/2500200/3-cerita-miris-korban-pemerkosaan-di-ethiopia-diperkosa-beramai-ramai-oleh-pemberontak')
