import requests
from bs4 import BeautifulSoup
import csv 

def get_book_informations(book_url, category_name) :

    url = book_url
    response = requests.get(url)

    book_info = {}

    if response.ok :
        soup = BeautifulSoup(response.text, 'lxml')

        book_page_url = response.url
        book_info["product_page_url"] = book_page_url

        book_description = ""
        book_description_tag = soup.find("article", {"class": "product_page"}).findChildren('p',recursive=False)
        for element in book_description_tag :
            book_description = element.text
        book_info["product_description"] = book_description

        book_title = soup.find('h1').text
        book_info["title"] = book_title

        image = soup.find("img")
        image_url = 'http://books.toscrape.com' + image['src']
        book_image_url = image_url.replace('../..','')
        book_info["image_url"] = book_image_url

        book_info_heading = ["universal_product_code(UPC)","category","price_excluding_tax","price_including_tax","tax","number_availaible","review_rating"]
        table_info = soup.find_all('td')
        book_info_extra = []
        for info in table_info :
            book_info_extra.append(info.text)

        extra_book_info = dict(zip(book_info_heading, book_info_extra))

        book_info.update(extra_book_info)
        book_info.pop("tax")

        with open(category_name + '.csv', 'a') as file:  
            w = csv.DictWriter(file, book_info.keys())
            if file.tell() == 0:
                w.writeheader()
            w.writerow(book_info)

        with open('images/' + book_title + '.jpg', 'wb') as handle:
            response = requests.get(book_image_url, stream=True)
            print(image_url)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)


def get_all_books_from_category(category_url, category_name):

    url = category_url
    response = requests.get(url)

    if response.ok :
        soup = BeautifulSoup(response.text, 'lxml')

        all_book_from_category = soup.find_all("h3")
        all_book_from_category_list = []
        for book in all_book_from_category :
            book_incomplete_url = book.find("a")["href"]
            book_page_url ='http://books.toscrape.com/catalogue' + book_incomplete_url.replace('../../..','')
            all_book_from_category_list.append(book_page_url)

        for url in all_book_from_category_list :
            get_book_informations(url, category_name)
            print(url)

        try :
            next_page_url = soup.find("li", {"class": "next"}).find("a")["href"]
            url_page = category_url.rsplit('/', 1)[-1]
            get_all_books_from_category(category_url.replace(url_page, next_page_url))
        except :
            pass


def get_all_category(page_url):

    url = page_url
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        all_category_from_page = soup.find("ul", {"class": "nav nav-list"}).find("li").find_all("a")

        all_category_from_page_url = {}
        for category in all_category_from_page:
            category_name_without_white_space = category.text.replace("\n", "")
            category_name = category_name_without_white_space.replace(" ", "")

            category_url = 'http://books.toscrape.com/catalogue/category/' + category["href"].replace('../','')

            all_category_from_page_url[category_name] = category_url
        all_category_from_page_url.pop("Books")

        for category_name in all_category_from_page_url :
            url = all_category_from_page_url[category_name]
            get_all_books_from_category(url, category_name)
            print(category_name)
            print(url)

get_all_category("http://books.toscrape.com/catalogue/category/books_1/index.html")


# url = "http://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
# response = requests.get(url)

# with open('images/pic1.jpg', 'wb') as handle:
#         response = requests.get(url, stream=True)

#         if not response.ok:
#             print(response)

#         for block in response.iter_content(1024):
#             if not block:
#                 break

#             handle.write(block)