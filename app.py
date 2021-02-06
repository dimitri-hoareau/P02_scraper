import requests
from bs4 import BeautifulSoup
import csv 

def get_book_informations(book_url) :
    # url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    url = book_url
    response = requests.get(url)

    book_info = {}

    if response.ok :
        soup = BeautifulSoup(response.text, 'lxml')

        book_page_url = response.url
        book_info["product_page_url"] = book_page_url

        book_description = soup.find_all("p")[-1].text.replace(",", " ")
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


        with open('book_info.csv', 'w') as f:  
            w = csv.DictWriter(f, book_info.keys())
            w.writeheader()
            w.writerow(book_info)




get_book_informations("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")