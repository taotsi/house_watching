import scrapy
from scrapy_splash import SplashRequest


class LinkSpider(scrapy.Spider):
    name = "link_spider"

    def start_requests(self):
        index_url = "http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/index.shtml"
        yield SplashRequest(url=index_url, callback=self.parse)

    def parse(self, response):
        items = response.xpath("//ul[@class='info-list']/li")
        for day_item in items:
            date = day_item.xpath(".//span/text()").get()
            if not date:
                continue
            url = day_item.xpath(".//a/@href").get()
            if not url:
                continue
            yield {
                "date": date,
                "url": url
            }

        next_page = response.xpath("//div[@class='black2']/a[contains(text(), '下一页')]/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SplashRequest(url=next_page, callback=self.parse)
