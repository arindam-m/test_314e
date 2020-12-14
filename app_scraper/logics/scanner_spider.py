import time

import scrapy
from scrapy.crawler import CrawlerProcess

start_time = time.time()


class ScannerSpider(scrapy.Spider):

    name = 'scanner_spider'

    root_index = 'https://www.314e.com/'
    start_urls = [root_index]

    webpage_links = [root_index]
    links_to_ignore = ['#', 'javascript:void(0);', root_index]

    custom_settings = {
        'DEPTH_LIMIT': 1,
        # 'FEED_URI': 'data.json',
    }

    def parse(self, response):

        # print(f"\nExisting settings: {self.settings.attributes.keys()}")

        for next_page in self.webpage_links:
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)

        # print("\n\n")
        # print(self.webpage_links)
        # print(len(self.webpage_links))
        # print(f"\nExecuted in {(time.time() - start_time):.2f} seconds.\n")
        # print("\n\n")

        yield {
            'url_list': self.webpage_links
        }

        for link in response.css('a::attr(href)').getall():
            if (link not in self.links_to_ignore
                    and link.startswith(self.root_index)
                    and link not in self.webpage_links):
                self.webpage_links.append(link)


# process = CrawlerProcess()
# process.crawl(ScannerSpider)
# process.start()
