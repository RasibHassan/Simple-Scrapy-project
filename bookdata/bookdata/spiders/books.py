from typing import Iterable
import scrapy
from pymongo import MongoClient

client=MongoClient("mongodb+srv://test:Hasan231@mongodb.epz4py0.mongodb.net/")

def save_to_mongo(page:str, title:str, price:str, rating:str):
    db=client["books"]
    collection=db[page]
    doc={
        "title":title,
        "price":price,
        "rating":rating
    }
    collection.insert_one(doc)

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls=[
            "https://books.toscrape.com/catalogue/category/books/religion_12/index.html",
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page=response.url.split("/")[-2]
        cards = response.css("article.product_pod")
        for card in cards:
            title=card.css("h3 a").attrib["title"]
            price=card.css("div.product_price p.price_color::text").get()
            rating=card.css("p.star-rating::attr(class)").get().split()[1]
            save_to_mongo(page, title, price, rating)

        pass
