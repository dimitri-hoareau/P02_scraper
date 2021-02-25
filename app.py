import requests
from bs4 import BeautifulSoup

from package.book_scraper import get_all_books_from_category

def get_all_category(page_url):

    """
    This function is used to scrap all book's category on the website called on parameter.
    For each category finded, it will call the function get_all_books_from_category(),
    imported from package.book_scraper.py
    """
    url = page_url
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')

        all_category_from_page = soup.find("ul", {"class": "nav nav-list"}).find("li").find_all("a")

        all_category_from_page_url = {}
        for category in all_category_from_page:
            category_name_without_white_space = category.text.replace("\n", "")
            category_name = category_name_without_white_space.replace(" ", "")

            category_url = ('http://books.toscrape.com/catalogue/category/' + category["href"]
            .replace('../',''))

            all_category_from_page_url[category_name] = category_url
        all_category_from_page_url.pop("Books")

        for category_name in all_category_from_page_url :
            print("*----------- getting all books and images from category : " + category_name + "---------------------*")
            url = all_category_from_page_url[category_name]
            get_all_books_from_category(url, category_name)


get_all_category("http://books.toscrape.com/catalogue/category/books_1/index.html")
