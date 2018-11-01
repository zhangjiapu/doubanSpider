import scrapy
from doubanSpider.items import DoubanItem
from scrapy.selector import Selector
from scrapy.http import Request
from urllib.parse import urljoin

class Douban(scrapy.spiders.Spider):
    name = "doubanspider"
    allowed_domains =  ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self,response):
        item = DoubanItem()
        selector = Selector(response)
        movies = selector.xpath("//div[@class = 'info']")
        for movie in movies:
            title = movie.xpath("div[@class = 'hd']/a/span/text()").extract()
            fullTitle = "".join(title)
            movieInfo = movie.xpath("div[@class = 'bd']/p/text()").extract()[0]
            star = movie.xpath("div[@class = 'bd']/div[@class = 'star']/span/text()").extract()[0]
            quote = movie.xpath("div[@class = 'bd']/p[@class = 'quote']/span/text()").extract()

            if quote:
                quote = quote[0]
            else:
                quote = ''

            item['title'] = fullTitle
            item['movieInfo'] = movieInfo
            item['star'] = star
            item['quote'] = quote

            yield item

        nextLink = selector.xpath("//span[@class = 'next']/a/@href").extract()

        if nextLink:
            nextLink = nextLink[0]
            yield Request(urljoin(response.url,nextLink),callback=self.parse)


