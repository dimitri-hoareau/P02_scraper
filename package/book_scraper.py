import os
import csv
import re
import requests
from bs4 import BeautifulSoup

def get_book_informations(book_url, category_name):

    """
    This function is used to get all book's information from a sepcific url.
    It will generate a csv named by the book's category name and add a line to this csv with all
    the book's information. It also get the image from the book page and save it in
    the repository "images"
    """

    url = book_url
    response = requests.get(url)

    book_info = {}

    def scrape_book_informations():
        soup = BeautifulSoup(response.content, 'html.parser')

        book_page_url = response.url
        book_info["product_page_url"] = book_page_url

        book_description = ""
        book_description_tag = (soup.find("article", {"class": "product_page"})
        .findChildren('p',recursive=False))

        for element in book_description_tag :
            book_description = element.text

        book_info["product_description"] = book_description

        book_title = soup.find('h1').text
        book_info["title"] = book_title

        image = soup.find("img")
        image_url = 'http://books.toscrape.com' + image['src']
        book_image_url = image_url.replace('../..','')
        book_info["image_url"] = book_image_url

        book_info_heading = [
            "universal_product_code(UPC)",
            "category","price_excluding_tax",
            "price_including_tax",
            "tax",
            "number_availaible",
            "review_rating"
            ]
        table_info = soup.find_all('td')
        book_info_extra = []
        for info in table_info :
            book_info_extra.append(info.text)

        extra_book_info = dict(zip(book_info_heading, book_info_extra))

        book_info.update(extra_book_info)
        book_info.pop("tax")

    def generate_csv():
        file_name = 'assets/' + category_name + '/' + category_name + '.csv'
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name,'a', encoding='utf-8') as file:
            writter = csv.DictWriter(file, book_info.keys())
            if file.tell() == 0:
                writter.writeheader()
            writter.writerow(book_info)

    def download_image():
        file_name = ('assets/' + category_name + '/' + re.sub(r'\W+', '_',
        book_info["title"]).lower() + '.jpg')
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'wb') as handle:
            response = requests.get(book_info["image_url"], stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    if response.ok :
        scrape_book_informations()
        generate_csv()
        download_image()


def get_all_books_from_category(category_url, category_name):

    """
    This function is used to get all books from a category. Then, for each book,
    it call the function get_book_informations().
    get_all_books_from_category() is a recursive function if the paging is over than 1,
    until the last page.
    """

    url = category_url
    response = requests.get(url)

    def scrape_category():
        soup = BeautifulSoup(response.content, 'html.parser')

        all_book_from_category = soup.find_all("h3")
        all_book_from_category_list = []
        for book in all_book_from_category :
            book_incomplete_url = book.find("a")["href"]
            book_page_url = ('http://books.toscrape.com/catalogue'
            + book_incomplete_url.replace('../../..',''))
            all_book_from_category_list.append(book_page_url)

        for url in all_book_from_category_list :
            get_book_informations(url, category_name)

        try :
            next_page_url = soup.find("li", {"class": "next"}).find("a")["href"]
            url_page = category_url.rsplit('/', 1)[-1]
            get_all_books_from_category(category_url.replace(url_page, next_page_url),category_name)
        except:
            pass

    if response.ok :
        scrape_category()
