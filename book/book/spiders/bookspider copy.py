import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
            for book in response.css('li.col-xs-6'):
                yield {
                    'title': book.css('h3 a::text').get(),
                    'link': response.urljoin(book.css('h3 a::attr(href)').get()),
                    'price': book.css('p.price_color::text').get()
                    }
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)