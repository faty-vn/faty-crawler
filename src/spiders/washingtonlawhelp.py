import requests
import scrapy


class WashingtonLawHelpSpider(scrapy.Spider):
    name = "wlh"
    allowed_domains = ["www.washingtonlawhelp.org"]
    base_url = 'https://www.washingtonlawhelp.org'
    start_urls = ["https://www.washingtonlawhelp.org/issues"]

    def parse(self, response):
        lst = response.css('#topic-list .card')

        for i in lst:
            major_url = i.xpath('@data-url').extract_first()
            yield scrapy.Request(url=f'{self.base_url}{major_url}', callback=self.parse_major)
            # break

    def parse_major(self, response):
        categories = response.css('#main-content .subtopic-list .card-title a')
        for category in categories:
            cate_url = category.xpath('@href').extract_first()

            yield scrapy.Request(url=f'{self.base_url}{cate_url}', callback=self.parse_category)
            # break

    def parse_category(self, response):
        articles = response.css('.card-body a')
        for article in articles:
            a_url = article.xpath('@href').extract_first()

            yield scrapy.Request(url=f'{self.base_url}{a_url}', callback=self.parse_article)
            # break

    def parse_article(self, response):
        download_link = response.css('.links .download-link').xpath('@href').extract_first()

        res = requests.get(f'{self.base_url}{download_link}')

        yield {
            'file_urls': [res.url]
        }
