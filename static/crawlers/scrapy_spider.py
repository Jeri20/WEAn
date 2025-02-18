# Scrapy Spider for website crawling
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class WebsiteSpider(CrawlSpider):
    name = "website_spider"
    allowed_domains = []
    start_urls = []
    rules = [Rule(LinkExtractor(), callback='parse_page', follow=True)]
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'DOWNLOAD_DELAY': 0.05,
        'COOKIES_ENABLED': False,
        'RETRY_ENABLED': False,
        'AUTOTHROTTLE_ENABLED': False,
        'DNS_RESOLVER': 'scrapy.resolver.CachingAsyncResolver',
        'ASYNCIO_EVENT_LOOP': 'uvloop',
        'DOWNLOAD_TIMEOUT': 30,
        'LOG_LEVEL': 'ERROR',
    }

    def parse_page(self, response):
        yield {'url': response.url,'title': response.xpath('//title/text()').get(),'headings': response.xpath('//h1//text() | //h2//text() | //h3//text()').getall(),'meta_description': response.xpath('//meta[@name="description"]/@content').get(),'content': ' '.join(response.xpath('//p//text()').getall())}
