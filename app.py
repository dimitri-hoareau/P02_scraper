import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


response = requests.get(url)

book_info = []
book_info_heading = []
book_info = []

if response.ok :
    soup = BeautifulSoup(response.text, 'lxml')

    book_page_url = response.url
    book_info_heading.append("product_page_url")
    book_info.append(book_page_url)

    book_description = soup.find_all("p")[-1].text.replace(",", " ")
    book_info_heading.append("product_description")
    book_info.append(book_description)

    title = soup.find('h1')
    book_title = title.text
    book_info_heading.append("title")
    book_info.append(book_title)

    image = soup.find("img")
    image_url = 'http://books.toscrape.com' + image['src']
    book_image_url = image_url.replace('../..','')
    book_info_heading.append("image_url")
    book_info.append(book_image_url)

    book_info_heading += ["universal_product_code(UPC)","category","price_excluding_tax","price_including_tax","number_availaible","review_rating"]

    # table_info_heading = soup.find_all('th')
    # for heading in table_info_heading :
    #     book_info_heading.append(heading.text)

    table_info = soup.find_all('td')
    for info in table_info :
        book_info.append(info.text)

    del book_info[8]

    with open("info.txt", "w") as infile :
        with open("book_info.csv", "w") as outfile :
            for heading in book_info_heading :
                outfile.write(heading + ",")
            outfile.write("\n")
            for info in book_info :
                outfile.write(info + ",")


