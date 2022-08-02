import scrapy
from scrapy.crawler import CrawlerProcess

class Flats500Spider(scrapy.Spider):
    name = 'flats500'
    custom_settings = {
        'ROBOTSTXT_OBEY' : False,
        'USER_AGENT' : 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
    allowed_domains = ['www.sreality.cz']
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20']

    def parse(self, response):
        flats_json = response.json()
        estates = flats_json['_embedded']['estates']
        for estate in estates:
            yield {"name": estate['name'], "location": estate['locality'], "image": estate['_links']['images'][0]['href']}
        