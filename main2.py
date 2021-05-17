from bs4 import BeautifulSoup
import requests

def get_page(url):
    return requests.get(url)
def get_nbr_pages(soup):
    pages = soup.find("div", class_="sc-116g21e-1 sc-116g21e-2 bepvzG euIWqN")
    pages = pages.find_all("a", class_="sc-1cf7u6r-0 Iqgxu sc-2y0ggl-1 LNJLu")
    return int(pages[-2].text)



def get_post(soup):
    price = soup.find("p", class_="sc-1x0vz2r-0 eXteHH")
    title = soup.find("h1", class_="sc-1x0vz2r-0 EJoJb").text
    description = soup.find('p', class_="ij98yj-0 jvMHNW").text

    surface = soup.find('span', class_="sc-1x0vz2r-0 eWvhPw").text


    if price != None:
       price = price.text
    else:
       price = "Price Not Specified"

    post = {
         'price': price ,
        'title': title ,
        'description': description ,
         'surface':surface }



    print(post)

def get_posts(soup): #afficher les lignes des annonces
    div_posts = soup.find("div", class_="sc-1nre5ec-0 fdVHEH").select("div[data-testid]")
    links = []
    for post in div_posts:
        links.append(post.find('a')['href'])

    posts = []
    for link in links:
        page = get_page(link)
        soup = BeautifulSoup(page.content, 'html.parser') #afficher le contenu des post en html
        posts.append(get_post(soup))

    return posts #cette methode il faut scraper les posts

if __name__ == '__main__':
    url = "https://www.avito.ma/fr/maroc/terrain--%C3%A0_vendre"
    page = get_page(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    nbr_pages = get_nbr_pages(soup)

    all_posts = []
    for i in range(1, 3):
        page_url = url + "?o=" + str(i)
        page = get_page(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_posts.append(get_posts(soup))

    print(all_posts)

