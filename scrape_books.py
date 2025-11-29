import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


def fetch_page(page_num):
    if page_num == 1:
        url = "http://books.toscrape.com/"
    else:
        url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        return None
    return BeautifulSoup(resp.text, "html.parser")

def parse_books(soup):
    books = []
    product_list = soup.find_all("article", class_="product_pod")
    for product in product_list:
        title = "N/A"
        price = "N/A"
        availability = "N/A"
        try:
            title = product.find("h3").find("a")["title"].strip()
        except Exception:
            title = "N/A"
        try:
            price_text = product.find("p", class_="price_color").text.strip()
            price = re.sub(r"[^\d.]", "", price_text) or "N/A"
        except Exception:
            price = "N/A"
        try:
            availability = product.find("p", class_="instock availability").text.strip()
        except Exception:
            availability = "N/A"
        books.append({"title": title, "price": price, "availability": availability})
    return books

if __name__ == "__main__":
    books_to_fetch = int(input("Enter the number of books you want to scrape : "))
    all_books = []
    page = 1
    while len(all_books) < books_to_fetch:
        soup = fetch_page(page)
        if soup is None:
            break
        books = parse_books(soup)
        if not books:
            break
        all_books.extend(books)
        time.sleep(random.uniform(2, 5))
        page += 1
    all_books = all_books[:books_to_fetch]
    df = pd.DataFrame(all_books)
    df.to_csv("books.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} books to books.csv")
