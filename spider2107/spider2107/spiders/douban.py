import scrapy
from scrapy import Request

from ..items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]

    # start_urls = ["https://movie.douban.com/top250?start=25&filter="]

    def start_requests(self):
        for i in range(0, 25, 25):
            yield Request(url=f"https://movie.douban.com/top250?start={i}&filter=", callback=self.parse)

    def parse(self, response, **kwargs):
        sel = scrapy.Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for item in list_items:
            href = item.css('div.hd > a::attr(href)').get()
            movie_item = MovieItem()
            movie_item["name"] = item.css('span.title::text').get()
            movie_item["author"] = item.css('div.bd > p::text').get()
            yield Request(url=href, meta={'movie_item': movie_item}, callback=self.parse_detail)

    def parse_detail(self, response, **kwargs):
        movie_item = response.meta['movie_item']
        movie_item['href'] = response.url
        movie_item['brief_introduction'] = response.css('#link-report-intra > span.all.hidden::text').get()
        yield movie_item
