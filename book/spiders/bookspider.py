import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css('li.col-xs-6.col-sm-4.col-md-3.col-lg-3'):
            book_page_link = book.css('h3 a::attr(href)').get()
            if book_page_link:
                yield response.follow(book_page_link, self.parse_book)


        next_page_url = response.css('li.next a::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, self.parse)

    def parse_book(self, response):
        yield {
            'title': response.css('div.product_main h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'availability': response.css('p.instock.availability::text').re_first(r'\d+ available'),
            'rating': response.css('p.star-rating::attr(class)').re_first(r'Star-rating\s(\w+)'),
            'upc': response.css('table.table-striped tr:nth-child(1) td::text').get(),
            'price_excl_tax': response.css('table.table-striped tr:nth-child(3) td::text').get(),
            'price_incl_tax': response.css('table.table-striped tr:nth-child(4) td::text').get(),
            'tax': response.css('table.table-striped tr:nth-child(5) td::text').get(),
            'number_of_reviews': response.css('table.table-striped tr:nth-child(7) td::text').get()
        }
