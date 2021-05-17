import json

from bs4 import BeautifulSoup
import requests


def get_page(url):
    return requests.get(url)


def get_nbr_pages(soup):
    pages = soup.find("div", class_="sc-116g21e-1 sc-116g21e-2 bepvzG euIWqN")
    pages = pages.find_all("a", class_="sc-1cf7u6r-0 Iqgxu sc-2y0ggl-1 LNJLu")
    return int(pages[-2].text)


def get_post(soup):

    script = soup.find("script", attrs={'id': '__NEXT_DATA__'}).string
    content_as_json = json.loads(script)
    post = {
        'category': content_as_json['props']['pageProps']['componentProps']['targetingArguments']['category'],
        'city': content_as_json['props']['pageProps']['componentProps']['targetingArguments']['city'],
        'subcat': content_as_json['props']['pageProps']['componentProps']['targetingArguments']['subcat'],
        'title': content_as_json['props']['pageProps']['componentProps']['targetingArguments']['title'],
        'type': content_as_json['props']['pageProps']['componentProps']['targetingArguments']['type'],
        'subject': content_as_json['props']['pageProps']['initialReduxState']['ad']['view']['adInfo']['subject'],
        'description': content_as_json['props']['pageProps']['initialReduxState']['ad']['view']['adInfo'][
            'description'],
        'phone': content_as_json['props']['pageProps']['initialReduxState']['ad']['view']['adInfo']['phone'],
        'price': content_as_json['props']['pageProps']['initialReduxState']['ad']['view']['adInfo']['price']['value'],
        'price_currency': content_as_json['props']['pageProps']['initialReduxState']['ad']['view']['adInfo']['price']['currency'],
    }


    return post


def get_posts(soup):
    div_posts = soup.find("div", class_="sc-1nre5ec-0 fdVHEH").select("div[data-testid]")
    links = []
    for post in div_posts:
        links.append(post.find('a')['href'])

    posts = []
    for link in links:
        page = get_page(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        posts.append(get_post(soup))

    return posts



if __name__ == '__main__':
    url = "https://www.avito.ma/fr/maroc/terrain--%C3%A0_vendre"
    page = get_page(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    nbr_pages = get_nbr_pages(soup)

    all_posts = []
    for i in range(1, 2):
        page_url = url + "?o=" + str(i)
        page = get_page(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_posts.append(get_posts(soup))

    print(all_posts)
